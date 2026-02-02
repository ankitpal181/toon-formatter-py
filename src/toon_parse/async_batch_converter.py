import asyncio
from typing import Literal
from .json_converter import json_to_toon, toon_to_json
from .yaml_converter import yaml_to_toon, toon_to_yaml
from .xml_converter import xml_to_toon, toon_to_xml
from .csv_converter import csv_to_toon, toon_to_csv
from .validator import validate_toon_string
from .encrypt import Encryptor
from .utils import async_batch_modulator


class AsyncBatchToonConverter:
    """
    Main converter class for easy usage.
    """

    def __init__(self, encryptor: Encryptor = None):
        self.encryptor = encryptor

    @async_batch_modulator
    async def from_json(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON-compatible data to TOON.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, json_to_toon, json_data)

    @async_batch_modulator
    async def to_json(self, toon_data: list[str] | str, return_json=True, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to JSON-compatible data.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_json, toon_data, return_json)

    @async_batch_modulator
    async def from_yaml(self, yaml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to TOON.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, yaml_to_toon, yaml_data)

    @async_batch_modulator
    async def to_yaml(self, toon_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to YAML.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_yaml, toon_data)

    @async_batch_modulator
    async def from_xml(self, xml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to TOON.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, xml_to_toon, xml_data)

    @async_batch_modulator
    async def to_xml(self, toon_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to XML.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_xml, toon_data)

    @async_batch_modulator
    async def from_csv(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to TOON.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, csv_to_toon, csv_data)

    @async_batch_modulator
    async def to_csv(self, toon_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert TOON to CSV.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_csv, toon_data)

    @staticmethod
    async def validate(toon_data: list[str] | str):
        """
        Validate a TOON string.
        """
        loop = asyncio.get_running_loop()

        if isinstance(toon_data, str):
            content = await loop.run_in_executor(None, lambda: open(toon_data, "r").read())
            return await loop.run_in_executor(None, validate_toon_string, content)
        else:
            return await asyncio.gather(*[loop.run_in_executor(None, validate_toon_string, datum) for datum in toon_data])
