"""
Module to run unit tests for pastesian package (which requires the installation of the `unittest` package).

To run this in the command-line, use `python -m unittest testing_pastesian.py`.
Alternatively, to get reports on how much of the code has been covered, use the `coverage` package through these
three commands (which requires the installation of the `coverage` package):
- `coverage run testing_pastesian.py`
- `coverage report`
- `coverage html`
"""

from pastesian import action_update_demand, solve, input_schema, output_schema
from pastesian.utils import check_each_period_id_column
from pastesian.main import create_optimization_parameters
import unittest
from math import isclose
import os
import pandas as pd
import inspect


def _this_directory():
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))


class TestPastesian(unittest.TestCase):
    period_id_field_name = 'Period ID'
    input_data_path = os.path.join(_this_directory(), "data/testing_data/1_input.json")
    output_data_path = os.path.join(_this_directory(), "data/testing_data/1_output.json")

    @classmethod
    def setUpClass(cls) -> None:
        cls.dat = input_schema.json.create_pan_dat(cls.input_data_path)
        cls.sln = output_schema.json.create_pan_dat(cls.output_data_path)

    def test_create_optimization_parameters(self):
        # Sample 1: original data set
        d, pc, ic, I = create_optimization_parameters(self.dat)
        I.sort()

        d_expected = {1: 200, 2: 350, 3: 150, 4: 250}
        pc_expected = {1: 5.5, 2: 7.2, 3: 8.8, 4: 10.9}
        ic_expected = {1: 1.3, 2: 1.95, 3: 2.2, 4: 2.0}
        I_expected = [1, 2, 3, 4]

        self.assertTrue(all(isclose(d[key], d_expected[key], rel_tol=1e-2) for key in d_expected))
        self.assertTrue(all(isclose(pc[key], pc_expected[key], rel_tol=1e-2) for key in pc_expected))
        self.assertTrue(all(isclose(ic[key], ic_expected[key], rel_tol=1e-2) for key in ic_expected))
        self.assertListEqual(I, I_expected)

        # Sample 2: demand['Period ID'] with more entries than costs['Period ID'], expected ValueError
        dat2 = input_schema.copy_pan_dat(self.dat)  # copy PanDat object
        demand_copy = dat2.demand.copy()
        demand_copy = pd.concat([demand_copy, pd.DataFrame([[5, 200]], columns=['Period ID', 'Demand'])])  # add new row
        dat2.demand = demand_copy  # update 'demand' table in dat2 PanDat object
        with self.assertRaises(ValueError):
            create_optimization_parameters(dat2)

        # Sample 3: costs['Period ID'] with more entries than demand['Period ID'], expected ValueError
        dat3 = input_schema.copy_pan_dat(self.dat)  # copy PanDat object
        costs_copy = dat3.costs.copy()
        costs_copy = pd.concat([costs_copy, pd.DataFrame(
            [[5, 7.8, 3.2]], columns=['Period ID', 'Production Cost', 'Inventory Cost']
            )
        ])  # add new row
        dat3.costs = costs_copy  # update 'costs' table in dat3 PanDat object
        with self.assertRaises(ValueError):
            create_optimization_parameters(dat3)

    def test_main_solve(self):
        # Test output data
        sln = solve(self.dat)

        # Expected output data
        production_flow_expected = self.sln.production_flow
        costs_expected = self.sln.costs

        # Testing
        self.assertIsNone(pd.testing.assert_frame_equal(sln.production_flow, production_flow_expected,
                                                        check_dtype=False, rtol=1.0e-5, atol=1.0e-8))
        self.assertIsNone(pd.testing.assert_frame_equal(sln.costs, costs_expected, check_dtype=False, rtol=1.0e-5,
                                                        atol=1.0e-8))

    def test_action_update_demand(self):
        # Safe operation
        demand_expected = self.dat.demand.copy()
        multiplier = -1  # default value for "Production Capacity", used in action_update_demand
        demand_expected['Demand'] = demand_expected['Demand'] * multiplier

        # Operation to test
        demand_to_test = action_update_demand(self.dat).demand

        # Testing
        self.assertIsNone(pd.testing.assert_frame_equal(demand_expected, demand_to_test, check_dtype=False,
                                                        rtol=1.0e-5, atol=1.0e-8))

    def test_check_each_period_id_column(self):
        # Sample 1: original good demand.csv
        self.assertIsNone(check_each_period_id_column(self.dat))

        # Sample 2: modified data with non-integers on demand['Period ID']
        dat2 = input_schema.copy_pan_dat(self.dat)
        dat2.demand[self.period_id_field_name] = dat2.demand[self.period_id_field_name] * 1.532
        with self.assertRaises(ValueError):
            check_each_period_id_column(dat2)

        # Sample 3: modified data with integer missing values on demand['Period ID']
        dat3 = input_schema.copy_pan_dat(self.dat)
        dat3.demand.drop(0, axis=0, inplace=True)  # remove first row
        with self.assertRaises(ValueError):
            check_each_period_id_column(dat3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
