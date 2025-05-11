import json
import os
from datetime import datetime
import requests

def get_guid():
    try:
        response = requests.get("https://www.uuidtools.com/api/generate/v1")
        if response.status_code == 200:
            return response.json()[0]
        else:
            return f"Error: Status code {response.status_code}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"

def log_error(filename, error_messages, log_file='error_log.json'):
    entry = {
        "guid": get_guid(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "filename": filename,
        "errors": error_messages
    }

    # If file exists, read old data, else start fresh
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(entry)

    with open(log_file, 'w') as f:
        json.dump(data, f, indent=4)

# Optional: test it
if __name__ == "__main__":
    sample_errors = ["Missing header", "Invalid reading value"]
    log_error("test_file.csv", sample_errors)
