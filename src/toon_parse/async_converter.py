import asyncio
from .json_converter import json_to_toon, toon_to_json
from .yaml_converter import yaml_to_toon, toon_to_yaml
from .xml_converter import xml_to_toon, toon_to_xml
from .csv_converter import csv_to_toon, toon_to_csv
from .validator import validate_toon_string
from typing import Literal
from .utils import async_encryption_modulator
from .encrypt import Encryptor

class AsyncToonConverter:
    """
    Async converter class for non-blocking usage.
    """

    def __init__(self, encryptor: Encryptor = None):
        self.encryptor = encryptor
    
    @async_encryption_modulator
    async def from_json(self, json_data, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON-compatible data to TOON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, json_to_toon, json_data)

    @async_encryption_modulator
    async def to_json(self, toon_string, return_json=True, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to JSON-compatible data (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_json, toon_string, return_json)

    @async_encryption_modulator
    async def from_yaml(self, yaml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to TOON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, yaml_to_toon, yaml_string)

    @async_encryption_modulator
    async def to_yaml(self, toon_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to YAML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_yaml, toon_string)

    @async_encryption_modulator
    async def from_xml(self, xml_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to TOON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, xml_to_toon, xml_string)

    @async_encryption_modulator
    async def to_xml(self, toon_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to XML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_xml, toon_string)

    @async_encryption_modulator
    async def from_csv(self, csv_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to TOON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, csv_to_toon, csv_string)

    @async_encryption_modulator
    async def to_csv(self, toon_string, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to CSV (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_csv, toon_string)

    @staticmethod
    async def validate(toon_string):
        """
        Validate a TOON string (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, validate_toon_string, toon_string)
