import csv, io


def validate_csv_string(csv_string):
    """
    Validates a CSV string for syntax and structural correctness.
    """
    validation_status = {'is_valid': True, 'error': None}

    if not csv_string or not isinstance(csv_string, str):
        validation_status = {'is_valid': False, 'error': 'Input must be a non-empty string.'}
    else:
        try:
            # syntax check
            csv.Sniffer().sniff(csv_string)

            # row length check
            f = io.StringIO(csv_string)
            reader = csv.reader(f)
            header = next(reader)
            expected_len = len(header)

            for i, row in enumerate(reader, start=2):
                if len(row) != expected_len:
                    raise ValueError(f"Error: Row {i} has {len(row)} columns, expected {expected_len}.")
        except ValueError as exception:
            validation_status = {'is_valid': False, 'error': str(exception)}

    return validation_status
