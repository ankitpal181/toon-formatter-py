from typing import Literal
from .json_converter import json_to_toon, toon_to_json
from .yaml_converter import yaml_to_toon, toon_to_yaml
from .xml_converter import xml_to_toon, toon_to_xml
from .csv_converter import csv_to_toon, toon_to_csv
from .validator import validate_toon_string
from .encrypt import Encryptor
from .utils import (
    encode_xml_reserved_chars, split_by_delimiter, parse_value, format_value,
    extract_json_from_string, extract_xml_from_string, extract_csv_from_string,
    encryption_modulator
)


class ToonConverter:
    """
    Main converter class for easy usage.
    """

    def __init__(self, encryptor: Encryptor = None):
        self.encryptor = encryptor

    @encryption_modulator
    def from_json(self, json_data, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON-compatible data to TOON.
        """
        return json_to_toon(json_data)

    @encryption_modulator
    def to_json(self, toon_string, return_json=True, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to JSON-compatible data.
        """
        return toon_to_json(toon_string, return_json)

    @encryption_modulator
    def from_yaml(self, yaml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to TOON.
        """
        return yaml_to_toon(yaml_string)

    @encryption_modulator
    def to_yaml(self, toon_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to YAML.
        """
        return toon_to_yaml(toon_string)

    @encryption_modulator
    def from_xml(self, xml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to TOON.
        """
        return xml_to_toon(xml_string)

    @encryption_modulator
    def to_xml(self, toon_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to XML.
        """
        return toon_to_xml(toon_string)

    @encryption_modulator
    def from_csv(self, csv_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to TOON.
        """
        return csv_to_toon(csv_string)

    @encryption_modulator
    def to_csv(self, toon_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
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
from .json_parse import JsonConverter, AsyncJsonConverter
from .yaml_parse import YamlConverter, AsyncYamlConverter
from .xml_parse import XmlConverter, AsyncXmlConverter
from .csv_parse import CsvConverter, AsyncCsvConverter

__all__ = [
    'ToonConverter', 'AsyncToonConverter',
    'JsonConverter', 'AsyncJsonConverter',
    'YamlConverter', 'AsyncYamlConverter',
    'XmlConverter', 'AsyncXmlConverter',
    'CsvConverter', 'AsyncCsvConverter',
    'json_to_toon', 'toon_to_json',
    'yaml_to_toon', 'toon_to_yaml',
    'xml_to_toon', 'toon_to_xml',
    'csv_to_toon', 'toon_to_csv',
    'validate_toon_string',
    'encode_xml_reserved_chars', 'split_by_delimiter', 'parse_value', 'format_value',
    'extract_json_from_string', 'extract_xml_from_string', 'extract_csv_from_string',
    'Encryptor'
]
