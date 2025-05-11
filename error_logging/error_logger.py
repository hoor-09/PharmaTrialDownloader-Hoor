import requests
import json
from datetime import datetime

LOG_FILE = "error_log.json"

def generate_guid():
    try:
        response = requests.get("https://www.uuidtools.com/api/generate/v1")
        if response.status_code == 200:
            return response.json()[0]
    except Exception as e:
        print(f"GUID generation error: {e}")
    return "GUID_ERROR"

def log_error(filename, error_description):
    log_entry = {
        "id": generate_guid(),
        "timestamp": datetime.now().isoformat(),
        "filename": filename,
        "error": error_description
    }
    with open(LOG_FILE, "a") as log:
        log.write(json.dumps(log_entry) + "\n")
