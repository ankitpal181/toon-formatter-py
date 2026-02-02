from typing import Literal
from ..yaml_converter import yaml_to_toon, toon_to_yaml
from ..json_parse import json_to_yaml, yaml_to_json
from .xml_converter import xml_to_yaml, yaml_to_xml
from .csv_converter import csv_to_yaml, yaml_to_csv
from .validator import validate_yaml_string
from ..encrypt import Encryptor
from ..utils import batch_modulator, run_in_parallel


class BatchYamlConverter:
    """
    Main converter class for easy usage.
    """

    def __init__(self, encryptor: Encryptor = None):
        self.encryptor = encryptor

    @batch_modulator
    def from_toon(self, toon_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert TOON to YAML.
        """
        return toon_to_yaml(toon_data)

    @batch_modulator
    def to_toon(self, yaml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert YAML to TOON.
        """
        return yaml_to_toon(yaml_data)

    @batch_modulator
    def from_json(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert JSON to YAML.
        """
        return json_to_yaml(json_data)

    @batch_modulator
    def to_json(self, yaml_data: list[str] | str, return_json=True, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert YAML to JSON.
        """
        return yaml_to_json(yaml_data, return_json)

    @batch_modulator
    def from_xml(self, xml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert XML to YAML.
        """
        return xml_to_yaml(xml_data)

    @batch_modulator
    def to_xml(self, yaml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert YAML to XML.
        """
        return yaml_to_xml(yaml_data)

    @batch_modulator
    def from_csv(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert CSV to YAML.
        """
        return csv_to_yaml(csv_data)

    @batch_modulator
    def to_csv(self, yaml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert YAML to CSV.
        """
        return yaml_to_csv(yaml_data)

    @staticmethod
    def validate(yaml_data: list[str] | str, parallel: bool = False):
        """
        Validate a YAML string.
        """
        if isinstance(yaml_data, str):
            with open(yaml_data, "r") as file:
                return validate_yaml_string(file.read())
        else:
            if parallel:
                return run_in_parallel(validate_yaml_string, None, yaml_data)
            else:
                return [validate_yaml_string(datum) for datum in yaml_data]
