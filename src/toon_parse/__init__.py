from .json_converter import json_to_toon, toon_to_json
from .yaml_converter import yaml_to_toon, toon_to_yaml
from .xml_converter import xml_to_toon, toon_to_xml
from .csv_converter import csv_to_toon, toon_to_csv
from .validator import validate_toon_string
from .utils import encode_xml_reserved_chars, split_by_delimiter, parse_value, format_value

class ToonConverter:
    """
    Main converter class for easy usage.
    """
    
    @staticmethod
    def from_json(json_data):
        """
        Convert JSON-compatible data to TOON.
        """
        return json_to_toon(json_data)

    @staticmethod
    def to_json(toon_string):
        """
        Convert TOON to JSON-compatible data.
        """
        return toon_to_json(toon_string)

    @staticmethod
    def from_yaml(yaml_string):
        """
        Convert YAML to TOON.
        """
        return yaml_to_toon(yaml_string)

    @staticmethod
    def to_yaml(toon_string):
        """
        Convert TOON to YAML.
        """
        return toon_to_yaml(toon_string)

    @staticmethod
    def from_xml(xml_string):
        """
        Convert XML to TOON.
        """
        return xml_to_toon(xml_string)

    @staticmethod
    def to_xml(toon_string):
        """
        Convert TOON to XML.
        """
        return toon_to_xml(toon_string)

    @staticmethod
    def from_csv(csv_string):
        """
        Convert CSV to TOON.
        """
        return csv_to_toon(csv_string)

    @staticmethod
    def to_csv(toon_string):
        """
        Convert TOON to CSV.
        """
        return toon_to_csv(toon_string)

    @staticmethod
    def validate(toon_string):
        """
        Validate a TOON string.
        """
        return validate_toon_string(toon_string)

from .async_converter import AsyncToonConverter

__all__ = [
    'ToonConverter', 'AsyncToonConverter',
    'json_to_toon', 'toon_to_json',
    'yaml_to_toon', 'toon_to_yaml',
    'xml_to_toon', 'toon_to_xml',
    'csv_to_toon', 'toon_to_csv',
    'validate_toon_string',
    'encode_xml_reserved_chars', 'split_by_delimiter', 'parse_value', 'format_value'
]
