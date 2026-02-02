from typing import Literal
from ..json_converter import json_to_toon, toon_to_json
from .yaml_converter import yaml_to_json, json_to_yaml
from .xml_converter import xml_to_json, json_to_xml
from .csv_converter import csv_to_json, json_to_csv
from .validator import validate_json_string
from ..encrypt import Encryptor
from ..utils import batch_modulator, run_in_parallel


class BatchJsonConverter:
    """
    Main converter class for easy usage.
    """

    def __init__(self, encryptor: Encryptor = None):
        self.encryptor = encryptor

    @batch_modulator
    def from_toon(self, toon_data: list[str] | str, return_json=True, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert TOON to JSON-compatible.
        """
        return toon_to_json(toon_data, return_json)

    @batch_modulator
    def to_toon(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert JSON-compatible data to TOON.
        """
        return json_to_toon(json_data)

    @batch_modulator
    def from_yaml(self, yaml_data: list[str] | str, return_json=True, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert YAML to JSON.
        """
        return yaml_to_json(yaml_data, return_json)

    @batch_modulator
    def to_yaml(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert JSON to YAML.
        """
        return json_to_yaml(json_data)

    @batch_modulator
    def from_xml(self, xml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert XML to JSON.
        """
        return xml_to_json(xml_data)

    @batch_modulator
    def to_xml(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert JSON to XML.
        """
        return json_to_xml(json_data)

    @batch_modulator
    def from_csv(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert CSV to JSON.
        """
        return csv_to_json(csv_data)

    @batch_modulator
    def to_csv(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert JSON to CSV.
        """
        return json_to_csv(json_data)

    @staticmethod
    def validate(json_data: list[str | dict | list] | str, parallel: bool = False):
        """
        Validate a JSON string.
        """

        if isinstance(json_data, str):
            with open(json_data, "r") as file:
                return validate_json_string(file.read())
        else:
            if parallel:
                return run_in_parallel(validate_json_string, None, json_data)
            else:
                return [validate_json_string(datum) for datum in json_data]
