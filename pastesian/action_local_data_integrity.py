from pastesian import input_schema


def local_data_integrity_check(dat):
    """
    The function checks all possible catches by ticdat package.

    :param dat: a PanDat object containing the data, usually the input data.
    :return:
    """

    # Foreign Key Failures
    print('-' * 30 + '\nForeign Key Failures\n' + '-' * 30)
    foreign_key_failures = input_schema.find_foreign_key_failures(dat, verbosity='Low')
    for key, value in foreign_key_failures.items():
        print(key)
        print(value)
        print()

    # Duplicate Rows
    print('-' * 30 + '\nDuplicate Rows Failures\n' + '-' * 30)
    duplicates = input_schema.find_duplicates(dat, keep='first')
    for table, rows in duplicates.items():
        print(f"Table = {table}")
        print(rows)
        print()

    # Data Rows Failures (Predicates)
    print('-' * 30 + '\nData Rows Failures (Predicates)\n' + '-' * 30)
    row_failures = input_schema.find_data_row_failures(dat)
    for key, value in row_failures.items():
        print(key)
        print(value)
        print()

    # Data Type Failures
    print('-' * 30 + '\nData Type Failures\n' + '-' * 30)
    data_type_failures = input_schema.find_data_type_failures(dat)
    for key, value in data_type_failures.items():
        print(key)
        print(value)
        print()
