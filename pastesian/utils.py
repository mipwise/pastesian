from pastesian import input_schema


def check_each_period_id_column(dat):
    """
    Check if all tables in dat object have the appropriate 'Period ID' column, i.e., integer numbers from 1 to the
    number of rows in the corresponding table, without any gap (but not necessarily ordered).

    Examples: I = [1, 4, 7, 5, 6, 3, 2] is a valid 'Period ID' column, while I = [3, 5, 4, 1] is not because number 2
    is missing in the latter.

    :param dat: PanDat object containing the input data, accordingly to the input_schema.

    :return:

    The function raises ValueError when an invalid 'Period ID' column is found.
    """
    field_name = 'Period ID'
    for table_name in input_schema.all_tables:
        table = dat.__getattribute__(table_name)

        # if hasattr(table, field_name):
        #     pass

        if field_name in table.columns:
            I = list(table[field_name])
            I.sort()
            if not I[0] == 1 or not I[-1] == len(I):
                error_msg = f"'{field_name}' column at '{table_name}' table must have all integers from 1 to the " \
                            f"biggest period index, not necessarily ordered though."
                raise ValueError(error_msg)


def check_period_id_matching():
    """
    Check if all tables share the same 'Period ID' column

    :return:
    """

    pass
