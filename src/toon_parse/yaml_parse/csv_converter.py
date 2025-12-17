import json
from ..utils import extract_csv_from_string
from ..json_parse import csv_to_json, json_to_csv


def csv_to_yaml(csv_string):
    """
    Converts CSV to YAML format.
    """
    if not csv_string or not isinstance(csv_string, str):
        raise ValueError("Input must be a non-empty string")
    
    converted_text = csv_string
    iteration_count = 0
    max_iterations = 100

    while iteration_count < max_iterations:
        csv_block = extract_csv_from_string(converted_text)
        if not csv_block: break

        try:
            data = json.loads(csv_to_json(csv_block))
            yaml_string = yaml.dump(data, sort_keys=False)
            yaml_output = yaml_string.strip()
            converted_text = converted_text.replace(csv_block, yaml_output)
            iteration_count += 1
        except:
            raise Exception('Error while converting CSV to YAML')

    return converted_text

def yaml_to_csv(yaml_string):
    """
    Converts YAML to CSV format.
    """
    if not yaml_string or not isinstance(yaml_string, str):
        raise ValueError("Input must be a non-empty string")
    
    try:
        data = yaml.safe_load(yaml_string)
        return json_to_csv(data)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {e}")
