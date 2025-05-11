import re

def is_valid_filename(filename):
    pattern = r"^MED_DATA_\d{14}\.csv$"
    return re.match(pattern, filename) is not None

def has_valid_headers(headers):
    expected = ["batch_id", "timestamp"] + [f"reading{i}" for i in range(1, 11)]
    return headers == expected

def has_duplicate_batch_ids(batch_ids):
    return len(batch_ids) != len(set(batch_ids))

def is_valid_reading(value):
    try:
        value = float(value)
        return 0.0 <= value <= 9.9
    except:
        return False
