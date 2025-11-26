import asyncio
from .json_converter import json_to_toon, toon_to_json
from .yaml_converter import yaml_to_toon, toon_to_yaml
from .xml_converter import xml_to_toon, toon_to_xml
from .csv_converter import csv_to_toon, toon_to_csv
from .validator import validate_toon_string

class AsyncToonConverter:
    """
    Async converter class for non-blocking usage.
    """
    
    @staticmethod
    async def from_json(json_data):
        """
        Convert JSON-compatible data to TOON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, json_to_toon, json_data)

    @staticmethod
    async def to_json(toon_string):
        """
        Convert TOON to JSON-compatible data (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_json, toon_string)

    @staticmethod
    async def from_yaml(yaml_string):
        """
        Convert YAML to TOON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, yaml_to_toon, yaml_string)

    @staticmethod
    async def to_yaml(toon_string):
        """
        Convert TOON to YAML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_yaml, toon_string)

    @staticmethod
    async def from_xml(xml_string):
        """
        Convert XML to TOON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, xml_to_toon, xml_string)

    @staticmethod
    async def to_xml(toon_string):
        """
        Convert TOON to XML (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, toon_to_xml, toon_string)

    @staticmethod
    async def from_csv(csv_string):
        """
        Convert CSV to TOON (Async).
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, csv_to_toon, csv_string)

    @staticmethod
    async def to_csv(toon_string):
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
