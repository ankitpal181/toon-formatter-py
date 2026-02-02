from typing import Literal
from ..xml_converter import xml_to_toon, toon_to_xml
from ..json_parse import json_to_xml, xml_to_json
from ..yaml_parse import xml_to_yaml, yaml_to_xml
from .csv_converter import csv_to_xml, xml_to_csv
from .validator import validate_xml_string
from ..encrypt import Encryptor
from ..utils import batch_modulator, run_in_parallel


class BatchXmlConverter:
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
        Convert TOON to XML.
        """
        return toon_to_xml(toon_data)

    @batch_modulator
    def to_toon(self, xml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert XML to TOON.
        """
        return xml_to_toon(xml_data)

    @batch_modulator
    def from_json(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert JSON to XML.
        """
        return json_to_xml(json_data)

    @batch_modulator
    def to_json(self, xml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert XML to JSON.
        """
        return xml_to_json(xml_data)

    @batch_modulator
    def from_yaml(self, yaml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert YAML to XML.
        """
        return yaml_to_xml(yaml_data)

    @batch_modulator
    def to_yaml(self, xml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert XML to YAML.
        """
        return xml_to_yaml(xml_data)

    @batch_modulator
    def from_csv(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert CSV to XML.
        """
        return csv_to_xml(csv_data)

    @batch_modulator
    def to_csv(self, xml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption", parallel: bool = False):
        """
        Convert XML to CSV.
        """
        return xml_to_csv(xml_data)

    @staticmethod
    def validate(xml_data: list[str] | str, parallel: bool = False):
        """
        Validate a XML string.
        """
        if isinstance(xml_data, str):
            with open(xml_data, "r") as file:
                return validate_xml_string(file.read())
        else:
            if parallel:
                return run_in_parallel(validate_xml_string, None, xml_data)
            else:
                return [validate_xml_string(datum) for datum in xml_data]
