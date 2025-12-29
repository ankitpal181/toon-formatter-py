import json
import xml.etree.ElementTree as ET
from ..utils import encode_xml_reserved_chars, extract_xml_from_string, extract_json_from_string, build_tag


def xml_to_json_object(element):
    """
    Converts XML Element to JSON object (recursive).
    """
    obj = {}
    
    # Attributes
    if element.attrib:
        obj["@attributes"] = element.attrib
    
    # Text content
    text = element.text.strip() if element.text else ""
    if text:
        # If no attributes and no children, return text directly?
        # JS logic: if (Object.keys(obj).length === 1 && obj['#text'] !== undefined) return obj['#text'];
        # But here we are building the object.
        # If we have attributes, text goes to #text.
        # If we have children, text goes to #text (if mixed content supported).
        pass

    has_children = len(element) > 0
    
    if has_children:
        for child in element:
            child_json = xml_to_json_object(child)
            tag = child.tag
            
            if tag not in obj:
                obj[tag] = child_json
            else:
                if not isinstance(obj[tag], list):
                    obj[tag] = [obj[tag]]
                obj[tag].append(child_json)
    
    # Handle text
    if text:
        if not has_children and not obj.get("@attributes"):
            return text
        obj["#text"] = text
        
    # If empty element
    if not obj and not text:
        return None # Or empty string? JS returns undefined if empty text node.
        # If element is <tag/>, JS returns {}?
        # JS: if (xml.hasChildNodes...) loop.
        # If no children, no attributes, no text -> empty object {}.
        return {}

    return obj

def xml_to_json(xml_string):
    """
    Converts XML to JSON format.
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
            # Encode reserved chars
            encoded_xml = encode_xml_reserved_chars(xml_block)
            # Parse XML
            # We wrap in a fake root if multiple roots? No, XML has one root.
            root = ET.fromstring(encoded_xml)
            
            # Convert to JSON object
            json_content = xml_to_json_object(root)
            data = {root.tag: json_content}
            json_string = json.dumps(data)
            json_output = json_string.strip()
            converted_text = converted_text.replace(xml_block, json_output)
            iteration_count += 1
        except:
            raise Exception('Error while converting XML to JSON')

    return converted_text

def json_to_xml(data):
    """
    Converts JSON to XML format.
    """
    if not data: raise ValueError("Input must be a non-empty")
    
    # Handle non-string input
    if not isinstance(data, str):
        xml_string = ""
        if isinstance(data, dict):
            for k, v in data.items():
                xml_string += build_tag(k, v)
        return xml_string

    converted_text = data
    iteration_count = 0
    max_iterations = 100

    while iteration_count < max_iterations:
        json_block = extract_json_from_string(converted_text)
        if not json_block: break
        
        try:
            xml_string = ""
            json_data = json.loads(json_block)
            if isinstance(json_data, dict):
                for k, v in json_data.items():
                    xml_string += build_tag(k, v)
            xml_output = xml_string.strip()
            converted_text = converted_text.replace(json_block, xml_output)
            iteration_count += 1
        except:
            raise Exception('Error while converting JSON to XML')
        
    return converted_text
