import os
import csv
import requests
from datetime import datetime
from google.oauth2.credentials import Credentials # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from googleapiclient.discovery import build # type: ignore
from googleapiclient.http import MediaFileUpload # type: ignore

# ------------------ Strategy Pattern for Validation ------------------

class ValidationStrategy:
    def validate(self, row): pass

class BasicValidation(ValidationStrategy):
    def validate(self, row):
        if any(not val.strip() for val in row.values()):
            return "Missing data"
        return None

class RangeValidation(ValidationStrategy):
    def validate(self, row):
        try:
            score = float(row['Score'])
            if not (0.0 <= score <= 9.9):
                return "Score out of range"
        except:
            return "Invalid score format"
        return None

class Validator:
    def __init__(self, strategies):
        self.strategies = strategies

    def validate(self, row):
        errors = []
        for strategy in self.strategies:
            result = strategy.validate(row)
            if result:
                errors.append(result)
        return errors

# ------------------ Google Drive Upload ------------------

def upload_to_gdrive(local_file_path):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': os.path.basename(local_file_path)}
    media = MediaFileUpload(local_file_path, mimetype='text/csv')

    uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = uploaded_file.get('id')
    print(f"Uploaded to Google Drive: File ID {file_id}")
    
    # Return shareable link format
    return f"https://drive.google.com/file/d/{file_id}/view"

# ------------------ Metadata API Tracker ------------------

def send_metadata(filename, status, storage_location=None):
    metadata = {
        "filename": filename,
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "storage_location": storage_location
    }
    response = requests.post("https://httpbin.org/post", json=metadata)
    if response.status_code == 200:
        print(f" Metadata sent: {metadata}")
    else:
        print(f" Failed to send metadata. Response: {response.status_code}")

# ------------------ Main Script ------------------

file_path = "csv_test_file.txt"
strategies = [BasicValidation(), RangeValidation()]
validator = Validator(strategies)

errors_found = False

with open(file_path, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        errors = validator.validate(row)
        if errors:
            print(f"Row {reader.line_num} errors: {errors}")
            errors_found = True
        else:
            print(f"Row {reader.line_num} is valid.")

# Upload and send metadata only if no errors
if not errors_found:
    file_link = upload_to_gdrive(file_path)
    send_metadata(file_path, "Valid", file_link)
else:
    send_metadata(file_path, "Invalid")