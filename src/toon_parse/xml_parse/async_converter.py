import asyncio
from typing import Literal
from ..xml_converter import xml_to_toon, toon_to_xml
from ..json_parse import json_to_xml, xml_to_json
from ..yaml_parse import xml_to_yaml, yaml_to_xml
from .csv_converter import csv_to_xml, xml_to_csv
from .validator import validate_xml_string
from ..encrypt import Encryptor
from ..utils import async_encryption_modulator


class AsyncXmlConverter:
    """
    Async converter class for non-blocking usage.
    """

    def __init__(self, encryptor: Encryptor = None):
        self.encryptor = encryptor
    
    @async_encryption_modulator
    async def from_toon(self, toon_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to XML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_xml, toon_string)

    @async_encryption_modulator
    async def to_toon(self, xml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to TOON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, xml_to_toon, xml_string)

    @async_encryption_modulator
    async def from_json(self, json_data, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON to XML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, json_to_xml, json_data)

    @async_encryption_modulator
    async def to_json(self, xml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to JSON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, xml_to_json, xml_string)

    @async_encryption_modulator
    async def from_yaml(self, yaml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to XML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, yaml_to_xml, yaml_string)

    @async_encryption_modulator
    async def to_yaml(self, xml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to YAML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, xml_to_yaml, xml_string)

    @async_encryption_modulator
    async def from_csv(self, csv_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to XML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, csv_to_xml, csv_string)

    @async_encryption_modulator
    async def to_csv(self, xml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to CSV (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, xml_to_csv, xml_string)

    @staticmethod
    async def validate(xml_string):
        """
        Validate a XML string (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, validate_xml_string, xml_string)
