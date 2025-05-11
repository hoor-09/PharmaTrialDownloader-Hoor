import csv
import os
import random
from datetime import datetime

# Create folders if they don't exist
VALID_DIR = "automation/test_data/valid"
INVALID_DIR = "automation/test_data/invalid"
os.makedirs(VALID_DIR, exist_ok=True)
os.makedirs(INVALID_DIR, exist_ok=True)

def get_current_timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')

def generate_valid_csv():
    filename = f"MED_DATA_{get_current_timestamp()}.csv"
    path = os.path.join(VALID_DIR, filename)
    headers = ["batch_id", "timestamp"] + [f"reading{i}" for i in range(1, 11)]

    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        used_batch_ids = set()
        for _ in range(10):
            batch_id = random.randint(1000, 9999)
            while batch_id in used_batch_ids:
                batch_id = random.randint(1000, 9999)
            used_batch_ids.add(batch_id)
            readings = [round(random.uniform(0.0, 9.8), 3) for _ in range(10)]
            writer.writerow([batch_id, datetime.now().strftime('%H:%M:%S')] + readings)

def generate_invalid_csv():
    filename = f"MED_DATA_{get_current_timestamp()}_BROKEN.csv"
    path = os.path.join(INVALID_DIR, filename)
    headers = ["batch", "time", "r1", "r2", "r3", "r4", "r5", "r6"]  # Wrong headers

    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        batch_id = 1000
        for _ in range(5):
            readings = [random.choice([10.0, -1.0, 11.5]) for _ in range(6)]
            writer.writerow([batch_id, datetime.now().strftime('%H:%M:%S')] + readings)

def generate_zero_byte_file():
    filename = f"MED_DATA_{get_current_timestamp()}_EMPTY.csv"
    path = os.path.join(INVALID_DIR, filename)
    open(path, 'w').close()

# Run the file generators
generate_valid_csv()
generate_invalid_csv()
generate_zero_byte_file()

print("Sample CSV files generated successfully.")
