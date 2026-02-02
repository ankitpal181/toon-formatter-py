from typing import Literal
from ..csv_converter import csv_to_toon, toon_to_csv
from ..json_parse import json_to_csv, csv_to_json
from ..yaml_parse import csv_to_yaml, yaml_to_csv
from ..xml_parse import csv_to_xml, xml_to_csv
from .validator import validate_csv_string
from ..encrypt import Encryptor
from ..utils import batch_modulator, run_in_parallel


class BatchCsvConverter:
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
        Convert TOON to CSV.
        """
        return toon_to_csv(toon_data)

    @batch_modulator
    def to_toon(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert CSV to TOON.
        """
        return csv_to_toon(csv_data)

    @batch_modulator
    def from_json(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert JSON to CSV.
        """
        return json_to_csv(json_data)

    @batch_modulator
    def to_json(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert CSV to JSON.
        """
        return csv_to_json(csv_data)

    @batch_modulator
    def from_yaml(self, yaml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert YAML to CSV.
        """
        return yaml_to_csv(yaml_data)

    @batch_modulator
    def to_yaml(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert CSV to YAML.
        """
        return csv_to_yaml(csv_data)

    @batch_modulator
    def from_xml(self, xml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert XML to CSV.
        """
        return xml_to_csv(xml_data)

    @batch_modulator
    def to_xml(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert CSV to XML.
        """
        return csv_to_xml(csv_data)

    @staticmethod
    def validate(csv_data: list[str] | str, parallel: bool = False):
        """
        Validate a CSV string.
        """
        if isinstance(csv_data, str):
            with open(csv_data, "r") as file:
                return validate_csv_string(file.read())
        else:
            if parallel:
                return run_in_parallel(validate_csv_string, None, csv_data)
            else:
                return [validate_csv_string(datum) for datum in csv_data]
