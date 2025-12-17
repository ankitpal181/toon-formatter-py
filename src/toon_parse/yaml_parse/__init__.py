from typing import Literal
from ..yaml_converter import yaml_to_toon, toon_to_yaml
from ..json_parse import json_to_yaml, yaml_to_json
from .xml_converter import xml_to_yaml, yaml_to_xml
from .csv_converter import csv_to_yaml, yaml_to_csv
from .validator import validate_yaml_string
from ..encrypt import Encryptor
from ..utils import encryption_modulator


class YamlConverter:
    """
    Main converter class for easy usage.
    """

    def __init__(self, encryptor: Encryptor = None):
        self.encryptor = encryptor

    @encryption_modulator
    def from_toon(self, toon_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to YAML.
        """
        return toon_to_yaml(toon_string)

    @encryption_modulator
    def to_toon(self, yaml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to TOON.
        """
        return yaml_to_toon(yaml_string)

    @encryption_modulator
    def from_json(self, json_data, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON to YAML.
        """
        return json_to_yaml(json_data)

    @encryption_modulator
    def to_json(self, yaml_string, return_json=True, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to JSON.
        """
        return yaml_to_json(yaml_string, return_json)

    @encryption_modulator
    def from_xml(self, xml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to YAML.
        """
        return xml_to_yaml(xml_string)

    @encryption_modulator
    def to_xml(self, yaml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to XML.
        """
        return yaml_to_xml(yaml_string)

    @encryption_modulator
    def from_csv(self, csv_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to YAML.
        """
        return csv_to_yaml(csv_string)

    @encryption_modulator
    def to_csv(self, yaml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to CSV.
        """
        return yaml_to_csv(yaml_string)

    @staticmethod
    def validate(yaml_string):
        """
        Validate a YAML string.
        """
        return validate_yaml_string(yaml_string)

from .async_converter import AsyncYamlConverter

__all__ = [
    'YamlConverter', 'AsyncYamlConverter',
    'xml_to_yaml', 'yaml_to_xml',
    'csv_to_yaml', 'yaml_to_csv',
]
