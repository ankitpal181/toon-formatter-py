import yaml, json
from ..utils import extract_json_from_string

def yaml_to_json(yaml_string, return_json=False):
    """
    Converts YAML to JSON format.
    """
    if not yaml_string or not isinstance(yaml_string, str):
        raise ValueError("Input must be a non-empty string")
    
    try:
        data = yaml.safe_load(yaml_string)
        return json.dumps(data) if return_json else data
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {e}")

def json_to_yaml(data):
    """
    Converts JSON to YAML format.
    """
    if not data: raise ValueError("Input must be a non-empty")
    
    # Handle non-string input
    if not isinstance(data, str): return yaml.dump(data, sort_keys=False)

    converted_text = data
    iteration_count = 0
    max_iterations = 100

    while iteration_count < max_iterations:
        json_block = extract_json_from_string(converted_text)
        if not json_block: break
        
        try:
            json_data = json.loads(json_block)
            yaml_string = yaml.dump(json_data, sort_keys=False)
            yaml_output = yaml_string.strip()
            converted_text = converted_text.replace(json_block, yaml_output)
            iteration_count += 1
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
        except:
            raise Exception('Error while converting JSON to YAML')

    return converted_text
