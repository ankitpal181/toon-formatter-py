import asyncio
from typing import Literal
from ..yaml_converter import yaml_to_toon, toon_to_yaml
from ..json_parse import json_to_yaml, yaml_to_json
from .xml_converter import xml_to_yaml, yaml_to_xml
from .csv_converter import csv_to_yaml, yaml_to_csv
from .validator import validate_yaml_string
from ..encrypt import Encryptor
from ..utils import async_batch_modulator


class AsyncBatchYamlConverter:
    """
    Async converter class for non-blocking usage.
    """

    def __init__(self, encryptor: Encryptor = None):
        self.encryptor = encryptor
    
    @async_batch_modulator
    async def from_toon(self, toon_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to YAML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_yaml, toon_data)

    @async_batch_modulator
    async def to_toon(self, yaml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to TOON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, yaml_to_toon, yaml_data)

    @async_batch_modulator
    async def from_json(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON to YAML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, json_to_yaml, json_data)

    @async_batch_modulator
    async def to_json(self, yaml_data: list[str] | str, return_json=True, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to JSON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, yaml_to_json, yaml_data, return_json)

    @async_batch_modulator
    async def from_xml(self, xml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to YAML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, xml_to_yaml, xml_data)

    @async_batch_modulator
    async def to_xml(self, yaml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to XML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, yaml_to_xml, yaml_data)

    @async_batch_modulator
    async def from_csv(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to YAML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, csv_to_yaml, csv_data)

    @async_batch_modulator
    async def to_csv(self, yaml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to CSV (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, yaml_to_csv, yaml_data)

    @staticmethod
    async def validate(yaml_data: list[str] | str):
        """
        Validate a YAML string (Async).
        """
        loop = asyncio.get_running_loop()

        if isinstance(yaml_data, str):
            content = await loop.run_in_executor(None, lambda: open(yaml_data, "r").read())
            return await loop.run_in_executor(None, validate_yaml_string, content)
        else:
            return await asyncio.gather(*[loop.run_in_executor(None, validate_yaml_string, datum) for datum in yaml_data])
