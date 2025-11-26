import yaml
from .json_converter import json_to_toon, toon_to_json

def yaml_to_toon(yaml_string):
    """
    Converts YAML to TOON format.
    """
    if not yaml_string or not isinstance(yaml_string, str):
        raise ValueError("Input must be a non-empty string")
    
    try:
        data = yaml.safe_load(yaml_string)
        return json_to_toon(data)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {e}")

def toon_to_yaml(toon_string):
    """
    Converts TOON to YAML format.
    """
    if not toon_string or not isinstance(toon_string, str):
        raise ValueError("Input must be a non-empty string")
    
    data = toon_to_json(toon_string)
    return yaml.dump(data, sort_keys=False)
