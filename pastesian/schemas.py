from ticdat import PanDatFactory

# region INPUT SCHEMA
input_schema = PanDatFactory(
    # table_name=[['Primary Key One', 'Primary Key Two', ...], ['Data Field One', 'Data Field Two', ...]]
    parameters=[['Parameter'], ['Value']],
    time_periods=[['Period ID'], ['Time Period']],
    demand=[['Period ID'], ['Demand']],
    costs=[['Period ID'], ['Production Cost', 'Inventory Cost']]
)

# endregion

# region USER PARAMETERS

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
# TODO: ensure 'Period ID' column will be like [1, 2, 3, 4, ...]
input_schema.set_data_type(table='time_periods', field='Time Period', number_allowed=False, strings_allowed=(),
                           datetime=True)

# endregion

# region demand table
input_schema.set_data_type(table='demand', field='Period ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=1.0, inclusive_min=True)
# TODO: ensure 'Period ID' column will be like [1, 2, 3, 4, ...]
input_schema.set_data_type(table='demand', field='Demand', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0.0, inclusive_min=True)
input_schema.add_foreign_key(native_table='demand', foreign_table='time_periods',
                             mappings=('Period ID', 'Period ID'))

# endregion

# region costs table
input_schema.set_data_type(table='costs', field='Period ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=1.0, inclusive_min=True)
# TODO: ensure 'Period ID' column will be like [1, 2, 3, 4, ...]
input_schema.set_data_type(table='costs', field='Production Cost', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=True)
input_schema.set_data_type(table='costs', field='Inventory Cost', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=True)
input_schema.add_foreign_key(native_table='costs', foreign_table='time_periods',
                             mappings=('Period ID', 'Period ID'))

# endregion

# endregion

# region DATA TYPES AND PREDICATES - OUTPUT SCHEMA

# region production_flow table
output_schema.set_data_type(table='production_flow', field='Period ID', number_allowed=True, strings_allowed=(),
                            must_be_int=True, min=1.0, inclusive_min=True)
# TODO: ensure 'Period ID' column will be like [1, 2, 3, 4, ...]
output_schema.set_data_type(table='production_flow', field='Production Quantity', number_allowed=True,
                            strings_allowed=(), must_be_int=True, min=0.0, inclusive_min=True)
output_schema.set_data_type(table='production_flow', field='Inventory Quantity', number_allowed=True,
                            strings_allowed=(), must_be_int=True, min=0.0, inclusive_min=True)

# endregion

# region costs table
output_schema.set_data_type(table='costs', field='Period ID', number_allowed=True, strings_allowed=(),
                            must_be_int=True, min=1.0, inclusive_min=True)
# TODO: ensure 'Period ID' column will be like [1, 2, 3, 4, ...]
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
