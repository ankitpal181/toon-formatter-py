import json


def validate_json_string(json_string):
    """
    Validates a JSON string for syntax and structural correctness.
    """
    validation_status = {'is_valid': True, 'error': None}

    if not json_string or not isinstance(json_string, str):
        validation_status = {'is_valid': False, 'error': 'Input must be a non-empty string.'}
    else:
        try:
            json.loads(json_string)
        except ValueError as exception:
            validation_status = {'is_valid': False, 'error': str(exception)}

    return validation_status
