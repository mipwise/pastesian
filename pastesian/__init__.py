__version__ = "0.1.3"
from pastesian.schemas import input_schema, output_schema
from pastesian.action_update_demand import action_update_demand
from pastesian.main import solve

__all__ = ['input_schema', 'output_schema', 'action_update_demand', 'solve']

input_tables_config = {
    'hidden_tables': ['parameters'],
    'categories': dict(),
    'order': ['time_periods', 'demand', 'costs'],
    'tables_display_names': dict(),
    'columns_display_names': {
        'costs': {'Production Cost': 'Production ($/unit)', 'Inventory Cost': 'Inventory ($/unit)'},
        },
    'hidden_columns': dict()
    }

output_tables_config = {
    'hidden_tables': list(),
    'categories': dict(),
    'order': list(),
    'tables_display_names': dict(),
    'columns_display_names': {
        'costs': {'Production Cost': 'Production ($)', 'Inventory Cost': 'Inventory ($)', 'Total Cost': 'Total ($)'}
    },
    'hidden_columns': dict()
    }

parameters_config = {
    'hidden': list(),
    'categories': dict(),
    'order': list(),
    'tooltips': {
        'Production Capacity': "Maximum number of lasagnas that can be produced throughout each period. Set it "
                               "to -1 (default) when there isn't such maximum production",
        'Inventory Capacity': "Maximum number of lasagnas that can be stored throughout each period. Set it "
                               "to -1 (default) when there isn't such maximum storage",
        'Lasagnas To Be Left': "Number of lasagnas expected at the end of the planning horizon, default=0",
        'Lasagnas To Start': "Number of lasagnas in the inventory at the beginning of the planning horizon, default=50"
        }
    }
