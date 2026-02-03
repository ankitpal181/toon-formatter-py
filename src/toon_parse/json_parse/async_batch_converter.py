import asyncio
from typing import Literal
from ..json_converter import json_to_toon, toon_to_json
from .yaml_converter import yaml_to_json, json_to_yaml
from .xml_converter import xml_to_json, json_to_xml
from .csv_converter import csv_to_json, json_to_csv
from .validator import validate_json_string
from ..encrypt import Encryptor
from ..utils import async_batch_modulator


class AsyncBatchJsonConverter:
    """
    Async converter class for non-blocking usage.
    """

    def __init__(self, encryptor: Encryptor = None):
        self.encryptor = encryptor
    
    @async_batch_modulator
    async def from_toon(self, toon_data: list[str] | str, return_json=True, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to JSON-compatible data (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_json, toon_data, return_json)

    @async_batch_modulator
    async def to_toon(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON-compatible data to TOON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, json_to_toon, json_data)

    @async_batch_modulator
    async def from_yaml(self, yaml_data: list[str] | str, return_json=True, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to JSON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, yaml_to_json, yaml_data, return_json)

    @async_batch_modulator
    async def to_yaml(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON to YAML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, json_to_yaml, json_data)

    @async_batch_modulator
    async def from_xml(self, xml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to JSON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, xml_to_json, xml_data)

    @async_batch_modulator
    async def to_xml(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON to XML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, json_to_xml, json_data)

    @async_batch_modulator
    async def from_csv(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to JSON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, csv_to_json, csv_data)

    @async_batch_modulator
    async def to_csv(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON to CSV (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, json_to_csv, json_data)

    @staticmethod
    async def validate(json_data: list[str | dict | list] | str):
        """
        Validate a JSON string (Async).
        """
        loop = asyncio.get_running_loop()

        if isinstance(json_data, str):
            content = await loop.run_in_executor(None, lambda: open(json_data, "r").read())
            return await loop.run_in_executor(None, validate_json_string, content)
        else:
            return await asyncio.gather(*[loop.run_in_executor(None, validate_json_string, datum) for datum in json_data])
