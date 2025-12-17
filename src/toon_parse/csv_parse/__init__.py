from typing import Literal
from ..csv_converter import csv_to_toon, toon_to_csv
from ..json_parse import json_to_csv, csv_to_json
from ..yaml_parse import csv_to_yaml, yaml_to_csv
from ..xml_parse import csv_to_xml, xml_to_csv
from .validator import validate_csv_string
from ..encrypt import Encryptor
from ..utils import encryption_modulator


class CsvConverter:
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
        Convert TOON to CSV.
        """
        return toon_to_csv(toon_string)

    @encryption_modulator
    def to_toon(self, csv_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to TOON.
        """
        return csv_to_toon(csv_string)

    @encryption_modulator
    def from_json(self, json_data, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON to CSV.
        """
        return json_to_csv(json_data)

    @encryption_modulator
    def to_json(self, csv_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to JSON.
        """
        return csv_to_json(csv_string)

    @encryption_modulator
    def from_yaml(self, yaml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to CSV.
        """
        return yaml_to_csv(yaml_string)

    @encryption_modulator
    def to_yaml(self, csv_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to YAML.
        """
        return csv_to_yaml(csv_string)

    @encryption_modulator
    def from_xml(self, xml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to CSV.
        """
        return xml_to_csv(xml_string)

    @encryption_modulator
    def to_xml(self, csv_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to XML.
        """
        return csv_to_xml(csv_string)

    @staticmethod
    def validate(csv_string):
        """
        Validate a CSV string.
        """
        return validate_csv_string(csv_string)

from .async_converter import AsyncCsvConverter

__all__ = [
    'CsvConverter', 'AsyncCsvConverter',
]
