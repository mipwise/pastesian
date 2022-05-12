from ticdat import PanDatFactory

# region INPUT SCHEMA
input_schema = PanDatFactory(
    # table_name=[['Primary Key One', 'Primary Key Two', ...], ['Data Field One', 'Data Field Two', ...]]
    parameters=[['Name'], ['Value']],
    time_periods=[['Period ID'], ['Time Period']],
    demand=[['Period ID'], ['Demand']],
    costs=[['Period ID'], ['Production Cost', 'Inventory Cost']]
)

# endregion

# region USER PARAMETERS
# Production Capacity: upper bound for monthly production
input_schema.add_parameter('Production Capacity', default_value=-1, number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=-1.0, inclusive_min=True)
# Inventory Capacity: upper bound for monthly storage
input_schema.add_parameter('Inventory Capacity', default_value=-1, number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=-1.0, inclusive_min=True)
# TODO: consider allowing production and inventory capacities to vary through periods, which would enter as input data

# When one of these capacity parameters is -1, it's like we didn't have the respective capacity restriction
input_schema.add_parameter('Lasagnas To Be Left', default_value=0, number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0.0, inclusive_min=True)  # Amount of lasagnas to be left in the
# last period
input_schema.add_parameter('Lasagnas To Start', default_value=50, number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0.0, inclusive_min=True)  # Amount of lasagnas we start with
# endregion

# region OUTPUT SCHEMA
output_schema = PanDatFactory(
    production_flow=[['Period ID'], ['Production Quantity', 'Inventory Quantity']],
    costs=[['Period ID'], ['Production Cost', 'Inventory Cost', 'Total Cost']]
)
# endregion

# region DATA TYPE AND PREDICATES - INPUT SCHEMA
# region time_periods table
input_schema.set_data_type(table='time_periods', field='Period ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=1.0, inclusive_min=True)

input_schema.set_data_type(table='time_periods', field='Time Period', number_allowed=False, strings_allowed=(),
                           datetime=True, nullable=True)
input_schema.add_foreign_key(native_table='time_periods', foreign_table='demand', mappings=('Period ID', 'Period ID'))
input_schema.add_foreign_key(native_table='time_periods', foreign_table='costs', mappings=('Period ID', 'Period ID'))

# endregion

# region demand table
input_schema.set_data_type(table='demand', field='Period ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=1.0, inclusive_min=True)
input_schema.set_data_type(table='demand', field='Demand', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0.0, inclusive_min=True)
input_schema.add_foreign_key(native_table='demand', foreign_table='time_periods',
                             mappings=('Period ID', 'Period ID'))
input_schema.set_default_value(table='demand', field='Demand', default_value=0)
# endregion

# region costs table
input_schema.set_data_type(table='costs', field='Period ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=1.0, inclusive_min=True)
input_schema.set_data_type(table='costs', field='Production Cost', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=True)
input_schema.set_data_type(table='costs', field='Inventory Cost', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=True)
input_schema.set_default_value(table='costs', field='Inventory Cost', default_value=0.00)
# TODO: this default_value at 'Inventory Cost' is temporary, fix it eventually because there seem to be no useful
#  default value to production and inventory costs.
# the above default value to inventory cost at costs table is to ensure that if the user doesn't want to have some
# left amount of lasagnas at the end of horizon, then he/she also doesn't want to insert some value to the inventory
# cost in the last period (which means the cost to storage from last period to next horizon, something we don't even
# want to do in this case).
input_schema.add_foreign_key(native_table='costs', foreign_table='time_periods', mappings=('Period ID', 'Period ID'))

# endregion

# endregion

# region DATA TYPES AND PREDICATES - OUTPUT SCHEMA

# region production_flow table
output_schema.set_data_type(table='production_flow', field='Period ID', number_allowed=True, strings_allowed=(),
                            must_be_int=True, min=1.0, inclusive_min=True)
output_schema.set_data_type(table='production_flow', field='Production Quantity', number_allowed=True,
                            strings_allowed=(), must_be_int=False, min=0.0, inclusive_min=True)
output_schema.set_data_type(table='production_flow', field='Inventory Quantity', number_allowed=True,
                            strings_allowed=(), must_be_int=False, min=0.0, inclusive_min=True)

# endregion

# region costs table
output_schema.set_data_type(table='costs', field='Period ID', number_allowed=True, strings_allowed=(),
                            must_be_int=True, min=1.0, inclusive_min=True)
output_schema.set_data_type(table='costs', field='Production Cost', number_allowed=True,
                            strings_allowed=(), must_be_int=False, min=0.0, inclusive_min=True)
output_schema.set_data_type(table='costs', field='Inventory Cost', number_allowed=True,
                            strings_allowed=(), must_be_int=False, min=0.0, inclusive_min=True)
output_schema.set_data_type(table='costs', field='Total Cost', number_allowed=True,
                            strings_allowed=(), must_be_int=False, min=0.0, inclusive_min=True)
output_schema.add_data_row_predicate(table='costs', predicate_name='Total Cost = Production Cost + Inventory Cost',
                                     predicate=lambda row: abs(row['Total Cost'] - row['Production Cost'] -
                                                               row['Inventory Cost']) <= 1e-2)

# endregion


# endregion
