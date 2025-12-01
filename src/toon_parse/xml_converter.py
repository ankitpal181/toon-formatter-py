import xml.etree.ElementTree as ET
from .json_converter import json_to_toon, toon_to_json
from .utils import encode_xml_reserved_chars, extract_xml_from_string

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

def json_object_to_xml(obj):
    """
    Converts JSON object to XML string (recursive).
    """
    xml_str = ""
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "#text":
                xml_str += str(value)
            elif key == "@attributes":
                # Handled by parent usually, but if we are here, we might need to handle it?
                # In JS, attributes are handled when processing the parent key.
                # But here we are iterating keys.
                # Wait, JS logic:
                # if (key === '@attributes' ...) -> adds to xml string.
                # But `xml` variable accumulates content.
                # If we have { "root": { "@attributes": {...}, "child": ... } }
                # We call jsonObjectToXml(root_val).
                # Inside: key="@attributes" -> adds attributes to... where?
                # JS: `xml += attrString`.
                # But this `xml` is the *inner content* of the tag?
                # No, JS `jsonObjectToXml` returns the inner content?
                # JS: `xml += <${key}${attrs}>${body}</${key}>`
                # Ah, if key is a tag name, it wraps it.
                # But if key is @attributes?
                # JS: `else if (key === '@attributes' ...)` -> `xml += attrString`.
                # This seems wrong in JS if it just appends attributes to the output string which is supposed to be a list of tags?
                # Wait, `jsonObjectToXml` returns a string of XML fragments.
                # If I have { "@attributes": {a:1}, "b": 2 }, it returns ` a="1"<b>2</b>`.
                # Then the parent wraps it: `<root a="1"><b>2</b></root>`.
                # Yes, that works.
                pass
                if isinstance(value, dict):
                    for attr_key, attr_val in value.items():
                         xml_str += f' {attr_key}="{attr_val}"'
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        inner_content = json_object_to_xml(item)
                        # Extract attributes from start of string if any
                        # This is a bit hacky in JS too: `innerContent.match(/^(\s+[^\s=]+="[^"]*")*/)`
                        # We need to separate attributes (which are at the start) from body.
                        # Attributes start with space. Body starts with < or text.
                        # But attributes are ` key="val"`.
                        
                        attrs = ""
                        body = inner_content
                        
                        # Simple parser for attributes at start
                        # Assuming attributes come first because of iteration order? 
                        # Dict order is insertion ordered in Python 3.7+.
                        # If @attributes is first, it works.
                        # If not, we might append attributes after body? That would be bad.
                        # We should probably process @attributes first.
                        
                        # But we are recursing.
                        # Let's refine `json_object_to_xml`.
                        pass
                        # Actually, let's rewrite to be more robust.
                        # We can't easily rely on string concatenation for attributes if they are mixed.
                        
                        # Better approach:
                        # If value is dict, check for @attributes inside it first.
                        pass
                    else:
                        xml_str += f"<{key}>{value}</{key}>"
            elif isinstance(value, dict):
                 # Nested object
                 inner_content = json_object_to_xml(value)
                 # Check for attributes at start
                 # This is tricky.
                 pass
            elif value is not None:
                xml_str += f"<{key}>{value}</{key}>"
    
    return xml_str

# Refined approach for json_to_xml_string to match JS logic better
def json_to_xml_string_v2(obj):
    xml_parts = []
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "#text":
                xml_parts.append(str(value))
                continue
            if key == "@attributes":
                # Return attributes string
                attr_parts = []
                for k, v in value.items():
                    attr_parts.append(f' {k}="{v}"')
                xml_parts.append("".join(attr_parts))
                continue
            
            # Normal tag
            if isinstance(value, list):
                for item in value:
                    xml_parts.append(build_tag(key, item))
            else:
                xml_parts.append(build_tag(key, value))

    return "".join(xml_parts)

def build_tag(key, value):
    if isinstance(value, dict):
        # We need to process children to separate attributes from content
        # But we can't easily separate them if we just recurse.
        # We should peek inside `value` for `@attributes`.
        attrs = ""
        content = ""
        
        # Process @attributes first
        if "@attributes" in value:
            attr_data = value["@attributes"]
            for k, v in attr_data.items():
                attrs += f' {k}="{v}"'
        
        # Process other keys
        for k, v in value.items():
            if k == "@attributes": continue
            if k == "#text":
                content += str(v)
            else:
                # Recurse
                if isinstance(v, list):
                    for item in v:
                        content += build_tag(k, item)
                else:
                    content += build_tag(k, v)
        
        return f"<{key}{attrs}>{content}</{key}>"
    
    elif value is not None:
        return f"<{key}>{value}</{key}>"
    else:
        return f"<{key} />"

def xml_to_toon(xml_string):
    """
    Converts XML to TOON format.
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
            # ElementTree root is the root element.
            # JS `xmlToJsonObject` takes the document.
            # If we pass root, we get the content of root.
            # We need to wrap it in the root tag name.
            
            json_content = xml_to_json_object(root)
            data = {root.tag: json_content}
            toon_string = json_to_toon(data)
            toon_output = toon_string.strip()
            converted_text = converted_text.replace(xml_block, toon_output)
            iteration_count += 1
        except:
            raise Exception('Error while converting XML to TOON')

    return converted_text

def toon_to_xml(toon_string):
    """
    Converts TOON to XML format.
    """
    if not toon_string or not isinstance(toon_string, str):
        raise ValueError("Input must be a non-empty string")
    
    data = toon_to_json(toon_string)
    
    # Convert to XML string
    # data is expected to be { "root": { ... } }
    # We use build_tag for the top level keys
    
    xml_str = ""
    if isinstance(data, dict):
        for k, v in data.items():
            xml_str += build_tag(k, v)
    
    return xml_str
