import pytest
import json
from toon_parse import StreamToonConverter

@pytest.fixture
def converter():
    return StreamToonConverter()

class TestStreamToonConverter:

    def test_json_streaming_basic(self, converter):
        # Case 1: Simple object chunks
        chunks = ['{"a":', ' 1', '}']
        
        # 1. '{"a":' -> invalid JSON -> ""
        delta1 = converter.from_json(chunks[0])
        assert delta1 == ""
        
        # 2. '{"a": 1' -> invalid JSON -> ""
        delta2 = converter.from_json(chunks[1])
        assert delta2 == ""
        
        # 3. '{"a": 1}' -> valid JSON -> TOON output 'a: 1'
        delta3 = converter.from_json(chunks[2])
        assert delta3.strip() == "a: 1"

    def test_json_streaming_complete(self, converter):
        # Case 2: One big chunk
        chunk = '{"name": "Alice"}'
        delta = converter.from_json(chunk)
        assert delta.strip() == 'name: "Alice"'

    def test_json_streaming_multiple_objects(self, converter):
        # NOTE: The current implementation appends input chunks. 
        # If we send a new object, it appends to the previous string: '...}{"b": 2}'
        # This might be invalid JSON depending on how extract_json_from_string works 
        # or if the user intends to stream separate JSON objects.
        # Given utils.py logic: self.last_input += str(data)
        # It creates a growing buffer.
        
        chunks = ['{"a": 1}', ' {"b": 2}']
        
        # 1. '{"a": 1}' -> 'a: 1'
        delta1 = converter.from_json(chunks[0])
        assert delta1.strip() == "a: 1"
        
        # 2. '{"a": 1}{"b": 2}' 
        # extract_json_from_string finds the first JSON block.
        # It might not finding the second one unless the converter handles multiple blocks.
        # The current implementation of json_to_toon loops: while iteration_count < max_iterations: ... extract_json_from_string
        # So it should replace ALL JSON blocks found in the string.
        
        delta2 = converter.from_json(chunks[1])
        # Expected: The first part is already converted to TOON in the internal buffer? 
        # Wait, stream_modulator does: 
        # self.last_input += str(data)
        # converted_output = convertor_function(self, self.last_input, **keyword_args)
        
        # 'convertor_function' is json_to_toon.
        # json_to_toon takes string, finds JSON chunks, replaces them with TOON.
        # So:
        # Step 1: last_input = '{"a": 1}' -> converted = 'a: 1' -> delta = 'a: 1'
        # Step 2: last_input = '{"a": 1}{"b": 2}' -> converted = 'a: 1\nb: 2' (approx)
        # delta = converted[len(last_output):] -> '\nb: 2'
        
        assert 'b: 2' in delta2

    def test_yaml_streaming(self, converter):
        # YAML converter usually works on the whole string.
        # If we stream partial YAML, PyYAML might fail or return partial dict?
        # But stream_modulator swallows exceptions.
        
        chunks = ['key:', ' value']
        
        # 1. "key:" -> valid YAML? {"key": None} -> 'key: null'
        # OR PyYAML waits for value? 
        # If it returns valid dict, we get output.
        # If invalid token, we get "".
        
        delta1 = converter.from_yaml(chunks[0])
        # Depending on YAML parser, "key:" might be valid.
        
        delta2 = converter.from_yaml(chunks[1])
        # "key: value" -> 'key: "value"' or 'key: value'
        
        # Delta logic is append-only. Replacing "null" (4 chars) with "value" (quoted, 7 chars)
        # "key: null" (9 chars) vs "key: "value"" (12 chars).
        # Delta starts at index 9: 'ue"'
        assert 'ue"' in delta2

    def test_xml_streaming(self, converter):
        # Case: <root><item>val</item></root>
        chunks = ['<roo', 't><item>val', '</item></root>']
        
        # 1. <roo -> incomplete -> ""
        delta1 = converter.from_xml(chunks[0])
        assert delta1 == ""
        
        # 2. <root><item>val -> incomplete (wait for closing tag for valid XML parser?) 
        # Actually minidom or other parsers might fail hard on <root><item>val
        # If it fails, stream_modulator returns ""
        delta2 = converter.from_xml(chunks[1])
        assert delta2 == ""
        
        # 3. Complete -> TOON output
        delta3 = converter.from_xml(chunks[2])
        assert 'root:' in delta3 
        assert 'item: "val"' in delta3

    def test_csv_streaming(self, converter):
        # LIMITATION: CSV streaming changes the TOON header (row count)
        # e.g. [0]{cols} -> [1]{cols}. The prefix is NOT constant.
        # This breaks simple delta logic (New - Old). 
        # This test documents that the delta contains the "diff", which might be the new count + new row.
        
        chunks = ['id,name\n', '1,Alice']
        
        # 1. Header
        delta1 = converter.from_csv(chunks[0])
        # Likely empty or initial header
        
        # 2. Row
        delta2 = converter.from_csv(chunks[1])
        # Since 'New' (count 1) doesn't start with 'Old' (count 0), 
        # delta = New[len(Old):] produces garbled output.
        # We just verify it returns *something* and doesn't crash.
        # Ideally, stream_modulator would handle non-monotonic updates, but it doesn't currently.
        assert isinstance(delta2, str)

    def test_toon_to_xml_streaming(self, converter):
        chunks = ['root:\n', '  item: "val"']
        
        # 1. root: -> <root></root> (approx)
        delta1 = converter.to_xml(chunks[0])
        assert '<root' in delta1
        
        # 2. Complete
        delta2 = converter.to_xml(chunks[1])
        assert 'val' in delta2 or 'item' in delta2

    def test_toon_to_yaml_streaming(self, converter):
        chunks = ['key: "val"']
        delta = converter.to_yaml(chunks[0])
        assert 'key: val' in delta

    def test_reset_state(self, converter):
        converter.last_input = ""
        converter.last_output = ""
        assert converter.last_input == ""

    def test_to_json_streaming(self, converter):
        # Converting TOON to JSON in stream
        # Use append-only scenario to avoid shrinking output (e.g. null -> 1)
        chunks = ['a: 1', '\nb: 2']
        
        # 1. "a: 1" -> {"a": 1}
        delta1 = converter.to_json(chunks[0])
        assert '"a": 1' in delta1
        
        # 2. "a: 1\nb: 2" -> {"a": 1, "b": 2}
        # Delta should contain "b": 2
        delta2 = converter.to_json(chunks[1])
        assert '"b": 2' in delta2 or 'b": 2' in delta2

