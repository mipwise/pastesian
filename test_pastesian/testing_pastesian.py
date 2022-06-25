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


class TestPastesian(unittest.TestCase):
    period_id_field_name = 'Period ID'
    input_path = os.path.join(os.path.dirname(__file__), "data/inputs")

    @classmethod
    def setUp(cls) -> None:
        cls.dat = input_schema.csv.create_pan_dat(cls.input_path)

    def test_create_optimization_parameters(self):
        pass

    def test_main_solve(self):
        self.assertEqual(1, 1)

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
