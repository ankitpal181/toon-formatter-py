import json, yaml
from ..utils import extract_xml_from_string
from ..json_parse import xml_to_json, json_to_xml


def xml_to_yaml(xml_string):
    """
    Converts XML to YAML format.
    """
    if not xml_string or not isinstance(xml_string, str):
        raise ValueError("Input must be a non-empty string")
    
    converted_text = xml_string
    iteration_count = 0
    max_iterations = 100

    while iteration_count < max_iterations:
        xml_block = extract_xml_from_string(converted_text)
        if not xml_block: break

        try:
            data = json.loads(xml_to_json(xml_block))
            yaml_string = yaml.dump(data, sort_keys=False)
            yaml_output = yaml_string.strip()
            converted_text = converted_text.replace(xml_block, yaml_output)
            iteration_count += 1
        except:
            raise Exception('Error while converting XML to YAML')

    return converted_text

def yaml_to_xml(yaml_string):
    """
    Converts YAML to XML format.
    """
    if not yaml_string or not isinstance(yaml_string, str):
        raise ValueError("Input must be a non-empty string")
    
    try:
        data = yaml.safe_load(yaml_string)
        return json_to_xml(data)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {e}")
