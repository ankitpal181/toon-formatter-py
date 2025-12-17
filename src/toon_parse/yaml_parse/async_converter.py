import asyncio
from typing import Literal
from ..yaml_converter import yaml_to_toon, toon_to_yaml
from ..json_parse import json_to_yaml, yaml_to_json
from .xml_converter import xml_to_yaml, yaml_to_xml
from .csv_converter import csv_to_yaml, yaml_to_csv
from .validator import validate_yaml_string
from ..encrypt import Encryptor
from ..utils import async_encryption_modulator


class AsyncYamlConverter:
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
        Convert TOON to YAML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_yaml, toon_string)

    @async_encryption_modulator
    async def to_toon(self, yaml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to TOON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, yaml_to_toon, yaml_string)

    @async_encryption_modulator
    async def from_json(self, json_data, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON to YAML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, json_to_yaml, json_data)

    @async_encryption_modulator
    async def to_json(self, yaml_string, return_json=True, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to JSON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, yaml_to_json, yaml_string, return_json)

    @async_encryption_modulator
    async def from_xml(self, xml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to YAML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, xml_to_yaml, xml_string)

    @async_encryption_modulator
    async def to_xml(self, yaml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to XML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, yaml_to_xml, yaml_string)

    @async_encryption_modulator
    async def from_csv(self, csv_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to YAML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, csv_to_yaml, csv_string)

    @async_encryption_modulator
    async def to_csv(self, yaml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to CSV (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, yaml_to_csv, yaml_string)

    @staticmethod
    async def validate(yaml_string):
        """
        Validate a YAML string (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, validate_yaml_string, yaml_string)
