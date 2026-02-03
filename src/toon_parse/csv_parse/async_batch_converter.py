import asyncio
from typing import Literal
from ..csv_converter import csv_to_toon, toon_to_csv
from ..json_parse import json_to_csv, csv_to_json
from ..yaml_parse import csv_to_yaml, yaml_to_csv
from ..xml_parse import csv_to_xml, xml_to_csv
from .validator import validate_csv_string
from ..encrypt import Encryptor
from ..utils import async_batch_modulator


class AsyncBatchCsvConverter:
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
        Convert TOON to CSV (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_csv, toon_data)

    @async_batch_modulator
    async def to_toon(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to TOON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, csv_to_toon, csv_data)

    @async_batch_modulator
    async def from_json(self, json_data: list[str | dict | list] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert JSON to CSV (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, json_to_csv, json_data)

    @async_batch_modulator
    async def to_json(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to JSON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, csv_to_json, csv_data)

    @async_batch_modulator
    async def from_yaml(self, yaml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert YAML to CSV (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, yaml_to_csv, yaml_data)

    @async_batch_modulator
    async def to_yaml(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to YAML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, csv_to_yaml, csv_data)

    @async_batch_modulator
    async def from_xml(self, xml_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert XML to CSV (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, xml_to_csv, xml_data)

    @async_batch_modulator
    async def to_xml(self, csv_data: list[str] | str, conversion_mode: Literal[
        "no_encryption", "middleware", "ingestion", "export"
    ] = "no_encryption"):
        """
        Convert CSV to XML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, csv_to_xml, csv_data)

    @staticmethod
    async def validate(csv_data: list[str] | str):
        """
        Validate a CSV string (Async).
        """
        loop = asyncio.get_running_loop()

        if isinstance(csv_data, str):
            content = await loop.run_in_executor(None, lambda: open(csv_data, "r").read())
            return await loop.run_in_executor(None, validate_csv_string, content)
        else:
            return await asyncio.gather(*[loop.run_in_executor(None, validate_csv_string, datum) for datum in csv_data])
