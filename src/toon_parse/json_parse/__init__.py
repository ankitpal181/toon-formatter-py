from typing import Literal
from ..json_converter import json_to_toon, toon_to_json
from .yaml_converter import yaml_to_json, json_to_yaml
from .xml_converter import xml_to_json, json_to_xml
from .csv_converter import csv_to_json, json_to_csv
from .validator import validate_json_string
from ..encrypt import Encryptor
from ..utils import encryption_modulator


class JsonConverter:
    """
    Main converter class for easy usage.
    """

    def __init__(self, encryptor: Encryptor = None):
        self.encryptor = encryptor

    @encryption_modulator
    def from_toon(self, toon_string, return_json=True, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to JSON-compatible.
        """
        return toon_to_json(toon_string, return_json)

    @encryption_modulator
    def to_toon(self, json_data, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON-compatible data to TOON.
        """
        return json_to_toon(json_data)

    @encryption_modulator
    def from_yaml(self, yaml_string, return_json=True, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to JSON.
        """
        return yaml_to_json(yaml_string, return_json)

    @encryption_modulator
    def to_yaml(self, json_data, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON to YAML.
        """
        return json_to_yaml(json_data)

    @encryption_modulator
    def from_xml(self, xml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to JSON.
        """
        return xml_to_json(xml_string)

    @encryption_modulator
    def to_xml(self, json_data, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON to XML.
        """
        return json_to_xml(json_data)

    @encryption_modulator
    def from_csv(self, csv_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to JSON.
        """
        return csv_to_json(csv_string)

    @encryption_modulator
    def to_csv(self, json_data, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON to CSV.
        """
        return json_to_csv(json_data)

    @staticmethod
    def validate(json_string):
        """
        Validate a JSON string.
        """
        return validate_json_string(json_string)

from .async_converter import AsyncJsonConverter

__all__ = [
    'JsonConverter', 'AsyncJsonConverter',
    'yaml_to_json', 'json_to_yaml',
    'xml_to_json', 'json_to_xml',
    'csv_to_json', 'json_to_csv',
]
