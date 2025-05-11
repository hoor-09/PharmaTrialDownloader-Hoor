import os
import csv
import shutil
from datetime import datetime
from validation import strategies
from error_logging.error_logger import log_error

DOWNLOADS_DIR = 'downloads'
STORAGE_DIR = 'storage'

def move_valid_file(file_path, filename):
    timestamp_str = filename.split('_')[2].split('.')[0]
    year = timestamp_str[0:4]
    month = timestamp_str[4:6]
    day = timestamp_str[6:8]

    target_dir = os.path.join(STORAGE_DIR, year, month, day)
    os.makedirs(target_dir, exist_ok=True)

    shutil.move(file_path, os.path.join(target_dir, filename))
    print(f"✅ Moved valid file to storage: {os.path.join(target_dir, filename)}")

def validate_file(file_path, filename):
    errors = []

    if os.path.getsize(file_path) == 0:
        errors.append("Empty file.")
        return errors

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)
        rows = list(reader)
        batch_ids = [row[0] for row in rows]
        readings = [r[2:] for r in rows]

    data_dict = {
        "filename": filename,
        "headers": headers,
        "rows": rows,
        "batch_ids": batch_ids,
        "readings": [val for sublist in readings for val in sublist]
    }

    validation_strategies = [
        ("Filename Check", lambda f, d: strategies.check_filename(f)),
        ("Header Check", lambda f, d: strategies.check_headers(d["headers"])),
        ("Duplicate Batch IDs", lambda f, d: strategies.check_no_duplicates(d["batch_ids"])),
        ("Reading Values", lambda f, d: strategies.check_readings(d["readings"])),
    ]

    for name, check in validation_strategies:
        if not check(filename, data_dict):
            errors.append(f"{name} failed")

    return errors

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
                print(f"Errors: {errors}")

if __name__ == "__main__":
    process_downloaded_files()
