import xml.etree.ElementTree as ET
from ..utils import encode_xml_reserved_chars


def validate_xml_string(xml_string):
    """
    Validates a XML string for syntax and structural correctness.
    """
    validation_status = {'is_valid': True, 'error': None}

    if not xml_string or not isinstance(xml_string, str):
        validation_status = {'is_valid': False, 'error': 'Input must be a non-empty string.'}
    else:
        try:
            # Encode reserved chars
            encoded_xml = encode_xml_reserved_chars(xml_string)
            # Parse XML
            ET.fromstring(encoded_xml)
        except Exception as exception:
            validation_status = {'is_valid': False, 'error': str(exception)}

    return validation_status
