from typing import Literal
from .json_converter import json_to_toon, toon_to_json
from .yaml_converter import yaml_to_toon, toon_to_yaml
from .xml_converter import xml_to_toon, toon_to_xml
from .csv_converter import csv_to_toon, toon_to_csv
from .validator import validate_toon_string
from .encrypt import Encryptor
from .utils import batch_modulator, run_in_parallel


class BatchToonConverter:
    """
    Main converter class for easy usage.
    """

    def __init__(self, encryptor: Encryptor = None):
        self.encryptor = encryptor

    @batch_modulator
    def from_json(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert JSON-compatible data to TOON.
        """
        return json_to_toon(json_data)

    @batch_modulator
    def to_json(self, toon_data: list[str] | str, return_json=True, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert TOON to JSON-compatible data.
        """
        return toon_to_json(toon_data, return_json)

    @batch_modulator
    def from_yaml(self, yaml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert YAML to TOON.
        """
        return yaml_to_toon(yaml_data)

    @batch_modulator
    def to_yaml(self, toon_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert TOON to YAML.
        """
        return toon_to_yaml(toon_data)

    @batch_modulator
    def from_xml(self, xml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert XML to TOON.
        """
        return xml_to_toon(xml_data)

    @batch_modulator
    def to_xml(self, toon_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert TOON to XML.
        """
        return toon_to_xml(toon_data)

    @batch_modulator
    def from_csv(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert CSV to TOON.
        """
        return csv_to_toon(csv_data)

    @batch_modulator
    def to_csv(self, toon_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert TOON to CSV.
        """
        return toon_to_csv(toon_data)

    @staticmethod
    def validate(toon_data: list[str] | str, parallel: bool = False):
        """
        Validate a TOON string.
        """
        if isinstance(toon_data, str):
            with open(toon_data, "r") as file:
                return validate_toon_string(file.read())
        else:
            if parallel:
                return run_in_parallel(validate_toon_string, None, toon_data)
            else:
                return [validate_toon_string(datum) for datum in toon_data]
