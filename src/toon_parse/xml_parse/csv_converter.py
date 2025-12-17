from ..utils import extract_csv_from_string, extract_xml_from_string
from ..json_parse import xml_to_json, json_to_xml, csv_to_json, json_to_csv


def csv_to_xml(csv_string):
    """
    Converts CSV to XML format.
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
            data = csv_to_json(csv_block)
            xml_string = json_to_xml(data)
            xml_output = xml_string.strip()
            converted_text = converted_text.replace(csv_block, xml_output)
            iteration_count += 1
        except:
            raise Exception('Error while converting CSV to XML')

    return converted_text

def xml_to_csv(xml_string):
    """
    Converts XML to CSV format.
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
            data = xml_to_json(xml_block)
            csv_string = json_to_csv(data)
            csv_output = csv_string.strip()
            converted_text = converted_text.replace(xml_block, csv_output)
            iteration_count += 1
        except:
            raise Exception('Error while converting XML to CSV')

    return converted_text
