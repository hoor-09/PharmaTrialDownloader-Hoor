from email import errors
from fileinput import filename
import os
import csv
import json
import shutil
from datetime import datetime
from validation.validation import is_valid_filename, has_valid_headers, has_duplicate_batch_ids, is_valid_reading
from error_logging.error_logger import log_error

DOWNLOADS_DIR = 'downloads'
STORAGE_DIR = 'storage'

def validate_file(file_path, filename):
    errors = []

    if not is_valid_filename(filename):
        errors.append("Invalid filename format.")

    if os.path.getsize(file_path) == 0:
        errors.append("Empty (0-byte) file.")
        return errors  # No need to check further if file is empty

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader, None)

        if not has_valid_headers(headers):
            errors.append("Invalid headers.")
            return errors

        batch_ids = []
        for row in reader:
            if len(row) != 12:
                errors.append("Row missing columns.")
                break

            batch_id = row[0]
            batch_ids.append(batch_id)

            readings = row[2:]
            for reading in readings:
                if not is_valid_reading(reading):
                    errors.append("Invalid reading value.")
                    break

        if has_duplicate_batch_ids(batch_ids):
            errors.append("Duplicate batch_id found.")

    return errors

def move_valid_file(file_path, filename):
    timestamp_str = filename.split('_')[2].split('.')[0]
    year = timestamp_str[0:4]
    month = timestamp_str[4:6]
    day = timestamp_str[6:8]

    target_dir = os.path.join(STORAGE_DIR, year, month, day)
    os.makedirs(target_dir, exist_ok=True)

    shutil.move(file_path, os.path.join(target_dir, filename))
    print(f"Moved valid file to storage: {os.path.join(target_dir, filename)}")

def process_downloaded_files():
    for filename in os.listdir(DOWNLOADS_DIR):
        file_path = os.path.join(DOWNLOADS_DIR, filename)

        if os.path.isfile(file_path):
            print(f"Validating file: {filename}")
            errors = validate_file(file_path, filename)

            if not errors:
                move_valid_file(file_path, filename)
            else:
                log_error(filename, "; ".join(errors))
                os.remove(file_path)
                print(f"Invalid file deleted: {filename}")

if __name__ == "__main__":
    process_downloaded_files()





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

# validate_and_store.py

from validation import strategies

validation_strategies = [
    ("Filename Check", lambda f, d: strategies.check_filename(f)),
    ("Header Check", lambda f, d: strategies.check_headers(d["headers"])),
    ("Duplicate Batch IDs", lambda f, d: strategies.check_no_duplicates(d["batch_ids"])),
    ("Reading Values", lambda f, d: strategies.check_readings(d["readings"])),
]

for name, check in validation_strategies:
    if not check(filename, data_dict): # type: ignore
        errors.append(f"{name} failed")
