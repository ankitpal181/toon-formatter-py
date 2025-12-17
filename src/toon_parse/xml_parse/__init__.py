from typing import Literal
from ..xml_converter import xml_to_toon, toon_to_xml
from ..json_parse import json_to_xml, xml_to_json
from ..yaml_parse import xml_to_yaml, yaml_to_xml
from .csv_converter import csv_to_xml, xml_to_csv
from .validator import validate_xml_string
from ..encrypt import Encryptor
from ..utils import encryption_modulator


class XmlConverter:
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
        Convert TOON to XML.
        """
        return toon_to_xml(toon_string)

    @encryption_modulator
    def to_toon(self, xml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to TOON.
        """
        return xml_to_toon(xml_string)

    @encryption_modulator
    def from_json(self, json_data, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON to XML.
        """
        return json_to_xml(json_data)

    @encryption_modulator
    def to_json(self, xml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to JSON.
        """
        return xml_to_json(xml_string)

    @encryption_modulator
    def from_yaml(self, yaml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to XML.
        """
        return yaml_to_xml(yaml_string)

    @encryption_modulator
    def to_yaml(self, xml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to YAML.
        """
        return xml_to_yaml(xml_string)

    @encryption_modulator
    def from_csv(self, csv_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to XML.
        """
        return csv_to_xml(csv_string)

    @encryption_modulator
    def to_csv(self, xml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to CSV.
        """
        return xml_to_csv(xml_string)

    @staticmethod
    def validate(xml_string):
        """
        Validate a XML string.
        """
        return validate_xml_string(xml_string)

from .async_converter import AsyncXmlConverter

__all__ = [
    'XmlConverter', 'AsyncXmlConverter',
    'csv_to_xml', 'xml_to_csv',
]
