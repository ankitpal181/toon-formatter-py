import csv
import io
from .json_converter import json_to_toon, toon_to_json

def csv_to_toon(csv_string):
    """
    Converts CSV to TOON format.
    """
    if not csv_string or not isinstance(csv_string, str):
        raise ValueError("Input must be a non-empty string")
    
    try:
        f = io.StringIO(csv_string)
        reader = csv.DictReader(f)
        data = list(reader)
        
        # Convert values to numbers/booleans/nulls if possible?
        # JS Papaparse has dynamicTyping: true usually?
        # The JS code uses `csvToToon` which likely uses `papaparse` with dynamic typing?
        # Let's check JS code if I can.
        # But for now, I'll stick to strings as csv module produces strings.
        # If I want to match TOON philosophy, I should probably try to infer types.
        # Let's add simple inference.
        
        parsed_data = []
        for row in data:
            new_row = {}
            for k, v in row.items():
                new_row[k] = _infer_type(v)
            parsed_data.append(new_row)
            
        return json_to_toon(parsed_data)
    except Exception as e:
        raise ValueError(f"Invalid CSV: {e}")

def _infer_type(val):
    if val is None: return None
    val = val.strip()
    if val == 'true': return True
    if val == 'false': return False
    if val == 'null': return None
    if val == '': return ""
    
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except ValueError:
        return val

def toon_to_csv(toon_string):
    """
    Converts TOON to CSV format.
    """
    if not toon_string or not isinstance(toon_string, str):
        raise ValueError("Input must be a non-empty string")
    
    data = toon_to_json(toon_string)
    
    if not isinstance(data, list):
        raise ValueError("TOON data must be an array of objects to convert to CSV")
    
    if not data:
        return ""
    
    # Collect all keys
    keys = set()
    for item in data:
        if isinstance(item, dict):
            keys.update(item.keys())
    
    fieldnames = sorted(list(keys)) # Sort for consistency
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in data:
        if isinstance(row, dict):
            writer.writerow(row)
            
    return output.getvalue().strip()
