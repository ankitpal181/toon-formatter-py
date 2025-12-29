import argparse
import sys
import asyncio
from .. import (
    ToonConverter, AsyncToonConverter,
    JsonConverter, AsyncJsonConverter,
    YamlConverter, AsyncYamlConverter,
    XmlConverter, AsyncXmlConverter,
    CsvConverter, AsyncCsvConverter,
    Encryptor
)

def main():
    parser = argparse.ArgumentParser(
        description="TOON Parse CLI - Convert between TOON, JSON, YAML, XML, and CSV."
    )
    
    parser.add_argument(
        "--from", dest="from_format", choices=["json", "yaml", "xml", "csv", "toon"],
        required=False, help="Source format"
    )
    parser.add_argument(
        "--to", dest="to_format", choices=["json", "yaml", "xml", "csv", "toon"],
        required=False, help="Target format"
    )
    parser.add_argument("-i", "--input", help="Input file path (default: stdin)")
    parser.add_argument("-o", "--output", help="Output file path (default: stdout)")
    parser.add_argument(
        "--async", dest="is_async", action="store_true",
        help="Use asynchronous converters"
    )
    parser.add_argument(
        "-m", "--mode", choices=["no_encryption", "middleware", "ingestion", "export"],
        default="no_encryption", help="Conversion mode"
    )
    parser.add_argument("-k", "--key", help="Encryption key")
    parser.add_argument(
        "-a", "--algo", default="fernet", help="Encryption algorithm (default: fernet)"
    )
    parser.add_argument(
        "--no-parse", action="store_true",
        help="Return raw JSON string instead of object (for Json/Yaml/Toon targets)"
    )
    parser.add_argument(
        "--validate", dest="format_to_validate", choices=["json", "yaml", "xml", "csv", "toon"],
        required=False, help="Validate format"
    )

    args = parser.parse_args()

    # Manual requirement check
    if not args.format_to_validate and (not args.from_format or not args.to_format):
        parser.error("The following arguments are required: --from and --to (unless --validate is used)")

    # Read Input
    if args.input:
        with open(args.input, 'r') as file:
            data = file.read()
    else:
        data = sys.stdin.read()

    if not data:
        print("Error: No input data provided.", file=sys.stderr)
        sys.exit(1)

    # Initialize Encryptor if needed
    encryptor = None
    if args.key:
        encryptor = Encryptor(key=args.key, algorithm=args.algo)

    # Setup Converter
    result = run_conversion(data, args, encryptor)
    
    # Handle Async Result
    if args.is_async and asyncio.iscoroutine(result):
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(result)

    # Write Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(str(result))
    else:
        sys.stdout.write(str(result))
        if not str(result).endswith('\n'):
            sys.stdout.write('\n')

def run_conversion(data, args, encryptor):
    if args.format_to_validate:
        return validate_format(data, args.format_to_validate, is_async=args.is_async, encryptor=encryptor)

    from_fmt = args.from_format
    to_fmt = args.to_format
    is_async = args.is_async
    mode = args.mode
    return_json = not args.no_parse

    # Set converter map
    if from_fmt == 'toon' or to_fmt == 'toon':
        conv = AsyncToonConverter(encryptor=encryptor) if is_async else ToonConverter(encryptor=encryptor)
        method_map = {
            ('json', 'toon'): conv.from_json,
            ('toon', 'json'): lambda d, **kwargs: conv.to_json(d, return_json=return_json, **kwargs),
            ('yaml', 'toon'): conv.from_yaml,
            ('toon', 'yaml'): conv.to_yaml,
            ('xml', 'toon'): conv.from_xml,
            ('toon', 'xml'): conv.to_xml,
            ('csv', 'toon'): conv.from_csv,
            ('toon', 'csv'): conv.to_csv,
        }
    elif from_fmt == 'json' or to_fmt == 'json':
        conv = AsyncJsonConverter(encryptor=encryptor) if is_async else JsonConverter(encryptor=encryptor)
        method_map = {
            ('json', 'yaml'): conv.to_yaml,
            ('json', 'xml'): conv.to_xml,
            ('json', 'csv'): conv.to_csv,
            ('yaml', 'json'): lambda d, **kwargs: conv.from_yaml(d, return_json=return_json, **kwargs),
            ('xml', 'json'): conv.from_xml,
            ('csv', 'json'): conv.from_csv,
        }
    elif from_fmt == 'yaml' or  to_fmt == 'yaml':
        conv = AsyncYamlConverter(encryptor=encryptor) if is_async else YamlConverter(encryptor=encryptor)
        method_map = {
            ('yaml', 'xml'): conv.to_xml,
            ('yaml', 'csv'): conv.to_csv,
            ('xml', 'yaml'): conv.from_xml,
            ('csv', 'yaml'): conv.from_yaml,
        }
    elif from_fmt == 'xml' or to_fmt == 'xml':
        conv = AsyncXmlConverter(encryptor=encryptor) if is_async else XmlConverter(encryptor=encryptor)
        method_map = {
            ('xml', 'csv'): conv.to_csv,
            ('csv', 'xml'): conv.from_csv,
        }
    else:
        print(f"Error: Unsupported conversion from {from_fmt} to {to_fmt}", file=sys.stderr)
        sys.exit(1)

    method = method_map.get((from_fmt, to_fmt))
    if not method:
        print(f"No implementation found for {from_fmt} to {to_fmt}", file=sys.stderr)
        sys.exit(1)

    try:
        return method(data, conversion_mode=mode)
    except TypeError:
        return method(data)

def validate_format(data, format_name, is_async=False, encryptor=None):
    if format_name == 'json':
        conv = AsyncJsonConverter(encryptor=encryptor) if is_async else JsonConverter(encryptor=encryptor)
    elif format_name == 'yaml':
        conv = AsyncYamlConverter(encryptor=encryptor) if is_async else YamlConverter(encryptor=encryptor)
    elif format_name == 'xml':
        conv = AsyncXmlConverter(encryptor=encryptor) if is_async else XmlConverter(encryptor=encryptor)
    elif format_name == 'csv':
        conv = AsyncCsvConverter(encryptor=encryptor) if is_async else CsvConverter(encryptor=encryptor)
    elif format_name == 'toon':
        conv = AsyncToonConverter(encryptor=encryptor) if is_async else ToonConverter(encryptor=encryptor)
    else:
        raise ValueError(f"Unsupported format: {format_name}")
    
    try:
        return conv.validate(data)
    except Exception as e:
        print(f"An error occurred while validating the format: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
