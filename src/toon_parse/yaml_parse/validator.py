import yaml


def validate_yaml_string(yaml_string):
    """
    Validates a YAML string for syntax and structural correctness.
    """
    validation_status = {'is_valid': True, 'error': None}

    if not yaml_string or not isinstance(yaml_string, str):
        validation_status = {'is_valid': False, 'error': 'Input must be a non-empty string.'}
    else:
        try:
            yaml.safe_load(yaml_string)
        except ValueError as exception:
            validation_status = {'is_valid': False, 'error': str(exception)}

    return validation_status
