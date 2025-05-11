import re

EXPECTED_HEADERS = [
    "batch_id", "timestamp",
    "reading1", "reading2", "reading3", "reading4", "reading5",
    "reading6", "reading7", "reading8", "reading9", "reading10"
]

def validate_filename(filename):
    pattern = r"MED_DATA_\d{14}\.csv"
    return bool(re.match(pattern, filename))

def validate_headers(headers):
    return headers == EXPECTED_HEADERS

def validate_batch_id_uniqueness(rows):
    seen = set()
    for row in rows:
        batch_id = row[0]
        if batch_id in seen:
            return False
        seen.add(batch_id)
    return True

def validate_reading_values(rows):
    try:
        for row in rows:
            readings = list(map(float, row[2:]))
            for value in readings:
                if not (0.0 <= value <= 9.9):
                    return False
    except ValueError:
        return False
    return True

def validate_not_empty(file_path):
    try:
        return os.path.getsize(file_path) > 0
    except Exception:
        return False

def check_filename(filename):
    return filename.startswith("MED_DATA_") and filename.endswith(".csv")

def check_headers(headers):
    expected = ["batch_id", "timestamp"] + [f"reading{i}" for i in range(1, 11)]
    return headers == expected

def check_no_duplicates(batch_ids):
    return len(batch_ids) == len(set(batch_ids))

def check_readings(readings):
    try:
        return all(0.0 <= float(r) <= 9.9 for r in readings)
    except:
        return False
