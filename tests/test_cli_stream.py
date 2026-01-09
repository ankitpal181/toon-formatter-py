import pytest
import argparse
from unittest.mock import MagicMock, patch
from toon_parse.cli import run_conversion, main

class TestCliStream:
    def test_conflict_async_stream(self):
        """Verify that --stream and --async cannot be used together."""
        with patch('sys.stderr', new=MagicMock()) as mock_stderr:
            with patch('sys.argv', ['cli', '--stream', '--async', '--from', 'json', '--to', 'toon']):
                with pytest.raises(SystemExit):
                    main()
        
    def test_json_to_toon_stream(self):
        """Verify basic JSON -> TOON conversion using StreamToonConverter via run_conversion."""
        args = argparse.Namespace(
            from_format='json',
            to_format='toon',
            is_async=False, # Conflict tested above
            is_stream=True,
            mode='no_encryption',
            no_parse=False,
            format_to_validate=None,
            input=None,
            output=None,
            key=None,
            algo='fernet'
        )
        data = '{"a": 1}'
        
        # Should return valid TOON string
        result = run_conversion(data, args, encryptor=None)
        assert 'a: 1' in result

    def test_toon_to_json_stream(self):
        """Verify basic TOON -> JSON conversion using StreamToonConverter via run_conversion."""
        args = argparse.Namespace(
            from_format='toon',
            to_format='json',
            is_async=False,
            is_stream=True,
            mode='no_encryption',
            no_parse=False,
            format_to_validate=None
        )
        data = 'a: 1'
        
        result = run_conversion(data, args, encryptor=None)
        # StreamToonConverter returns the text delta, i.e., the JSON string.
        # It does NOT return a dict even if return_json=True is requested,
        # because stream_modulator handles string I/O.
        # However, checking the failure provided by the user ('{"a": 1}' which is a string),
        # confirms it returns a string.
        
        assert isinstance(result, str)
        assert '"a": 1' in result or "'a': 1" in result

    def test_stream_flag_ignored_for_non_toon(self):
        """
        The CLI code only checks is_stream if format is TOON.
        If we provide --stream for json->yaml, it should fall back to non-stream (or ignore).
        Validation: The CLI logic:
        if from_fmt == 'toon' or to_fmt == 'toon': ...
        elif ...
        
        So if we do json->yaml, it goes to elif from_fmt == 'json' ...
        and uses standard JsonConverter.
        """
        args = argparse.Namespace(
            from_format='json',
            to_format='yaml',
            is_async=False,
            is_stream=True, # Should be ignored effectively
            mode='no_encryption',
            no_parse=False,
            format_to_validate=None
        )
        data = '{"a": 1}'
        result = run_conversion(data, args, encryptor=None)
        assert 'a: 1' in result

