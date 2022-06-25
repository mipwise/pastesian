from pastesian import input_schema


def check_each_period_id_column(dat):
    """
    Check if all tables in dat object have the appropriate 'Period ID' column, i.e., integer numbers from 1 to the
    number of rows in the corresponding table, without any gap (but not necessarily ordered).

    Examples: I = [1, 4, 7, 5, 6, 3, 2] is a valid 'Period ID' column, while I = [3, 5, 4, 1] is not because number 2
    is missing in the latter.

    Parameters
    ----------
    dat : PanDat
        A PanDat object containing the input data, accordingly to the input_schema.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        It's raised in two situations: 1) when some 'Period ID' column with non-integer values is found; when an invalid
        'Period ID' column is found, that is, some 'Period ID' column containing missing value(s). It reports table and
        field names in the error message.

    """
    field_name = 'Period ID'
    for table_name in input_schema.all_tables:
        table = dat.__getattribute__(table_name)
        if field_name in table.columns:
            # Check for list of integer values
            I = list(table[field_name])
            if not all(isinstance(item, int) for item in I):
                raise ValueError(f"{table_name}['{field_name}'] field only accepts integer values!")

            # Check if there is any missing value
            I.sort()
            aux_list = list(range(1, len(I)+1))  # list from 1 to len(I)
            if not I == aux_list:
                raise ValueError(f"{table_name}['{field_name}'] field must have all integers from 1 to {len(I)}, "
                                 f"not necessarily ordered.")

