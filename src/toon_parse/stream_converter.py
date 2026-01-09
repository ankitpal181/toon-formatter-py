from .json_converter import json_to_toon, toon_to_json
from .yaml_converter import yaml_to_toon, toon_to_yaml
from .xml_converter import xml_to_toon, toon_to_xml
from .csv_converter import csv_to_toon, toon_to_csv
from .utils import stream_modulator


class StreamToonConverter:
    """
    Main converter class for easy usage.
    """

    def __init__(self):
        self.last_input = ""
        self.last_output = ""

    @stream_modulator
    def from_json(self, json_data):
        """
        Convert JSON-compatible data to TOON.
        """
        return json_to_toon(json_data)

    @stream_modulator
    def to_json(self, toon_string, return_json=True):
        """
        Convert TOON to JSON-compatible data.
        """
        return toon_to_json(toon_string, return_json)

    @stream_modulator
    def from_yaml(self, yaml_string):
        """
        Convert YAML to TOON.
        """
        return yaml_to_toon(yaml_string)

    @stream_modulator
    def to_yaml(self, toon_string):
        """
        Convert TOON to YAML.
        """
        return toon_to_yaml(toon_string)

    @stream_modulator
    def from_xml(self, xml_string):
        """
        Convert XML to TOON.
        """
        return xml_to_toon(xml_string)

    @stream_modulator
    def to_xml(self, toon_string):
        """
        Convert TOON to XML.
        """
        return toon_to_xml(toon_string)

    @stream_modulator
    def from_csv(self, csv_string):
        """
        Convert CSV to TOON.
        """
        return csv_to_toon(csv_string)

    @stream_modulator
    def to_csv(self, toon_string):
        """
        Convert TOON to CSV.
        """
        return toon_to_csv(toon_string)
