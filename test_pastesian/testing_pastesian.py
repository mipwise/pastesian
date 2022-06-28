"""
Module to run unit tests for pastesian package.

Commands for the command-line:

- coverage run <test_file.py>
- coverage report
- coverage html
"""

from pastesian import action_update_demand, solve, input_schema
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
    input_path = os.path.join(_this_directory(), "data/inputs")

    @classmethod
    def setUp(cls) -> None:
        cls.dat = input_schema.csv.create_pan_dat(cls.input_path)

    def test_create_optimization_parameters(self):
        # Original data set
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

        # demand['Period ID'] with more entries than costs['Period ID']
        dat2 = input_schema.copy_pan_dat(self.dat)  # copy PanDat object
        demand_copy = dat2.demand.copy()
        demand_copy = pd.concat([demand_copy, pd.DataFrame([[5, 200]], columns=['Period ID', 'Demand'])])  # add new row
        dat2.demand = demand_copy  # update 'demand' table in dat2 PanDat object

        with self.assertRaises(ValueError):
            d, pc, ic, I = create_optimization_parameters(dat2)

        # costs['Period ID'] with more entries than demand['Period ID']
        dat3 = input_schema.copy_pan_dat(self.dat)  # copy PanDat object
        costs_copy = dat3.costs.copy()
        costs_copy = pd.concat([costs_copy, pd.DataFrame(
            [[5, 7.8, 3.2]], columns=['Period ID', 'Production Cost', 'Inventory Cost']
            )
        ])  # add new row
        dat3.costs = costs_copy  # update 'costs' table in dat3 PanDat object

        with self.assertRaises(ValueError):
            d, pc, ic, I = create_optimization_parameters(dat3)

    def test_main_solve(self):
        # Test output data
        sln = solve(self.dat)

        # Expected output data
        production_flow_expected = pd.read_csv(os.path.join(_this_directory(), "data/outputs/production_flow.csv"))
        costs_expected = pd.read_csv(os.path.join(_this_directory(), "data/outputs/costs.csv"))

        # Testing
        self.assertIsNone(pd.testing.assert_frame_equal(sln.production_flow, production_flow_expected,
                                                        check_dtype=False, rtol=1.0e-5, atol=1.0e-8))
        self.assertIsNone(pd.testing.assert_frame_equal(sln.costs, costs_expected, check_dtype=False, rtol=1.0e-5,
                                                        atol=1.0e-8))


    def test_action_update_demand(self):
        # Safe operation
        demand_copy = self.dat.demand.copy()
        multiplier = -1  # default value for "Production Capacity", which is used in action_update_demand
        demand_copy['Demand'] = demand_copy['Demand'] * multiplier

        # Operation to test
        self.dat = action_update_demand(self.dat)

        num_rows = demand_copy.shape[0]
        for index in range(num_rows):
            action_output = self.dat.demand.at[index, 'Demand']
            expected_output = demand_copy.at[index, 'Demand']
            self.assertTrue(isclose(action_output, expected_output, rel_tol=1e-2),
                            msg=f'action: {action_output}, expected: {expected_output}')

    def test_check_each_period_id_column(self):
        # Original good demand.csv
        self.assertIsNone(check_each_period_id_column(self.dat))

        # Non-integers on demand['Period ID']
        self.dat.demand[self.period_id_field_name] = self.dat.demand[self.period_id_field_name] * 1.532
        with self.assertRaises(ValueError):
            check_each_period_id_column(self.dat)

        # Integer missing values on demand['Period ID']
        self.dat = input_schema.csv.create_pan_dat(self.input_path)  # reset self.dat object
        self.dat.demand.drop(0, axis=0, inplace=True)
        with self.assertRaises(ValueError):
            check_each_period_id_column(self.dat)

        # We don't need a Bad PanDat object case, because when we call the check_each_period_id_column function,
        # we have already created the PanDat object through input_schema.csv.create_pan_dat (or similar to xls file)
        # so that TicDat would have already raised error for bad PanDat


if __name__ == '__main__':
    unittest.main(verbosity=2)
