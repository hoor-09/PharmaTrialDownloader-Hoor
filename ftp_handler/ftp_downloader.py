import ftplib
import os
import json

FTP_SERVER = 'ftp.example.com'  # Replace with actual server (if available)
FTP_USER = 'username'           # Replace with actual username
FTP_PASSWORD = 'password'       # Replace with actual password
FTP_DIRECTORY = '/csvfiles/'    # Directory containing CSV files
LOCAL_DOWNLOAD_DIR = 'downloads/'  # Local folder to save files
TRACKING_FILE = 'processed_files.json'

# Create local download folder if it doesn't exist
os.makedirs(LOCAL_DOWNLOAD_DIR, exist_ok=True)

# Create processed_files.json if it doesn't exist
if not os.path.exists(TRACKING_FILE):
    with open(TRACKING_FILE, 'w') as f:
        json.dump([], f)

def load_processed_files():
    with open(TRACKING_FILE, 'r') as f:
        return json.load(f)

def save_processed_file(filename):
    processed = load_processed_files()
    processed.append(filename)
    with open(TRACKING_FILE, 'w') as f:
        json.dump(processed, f)

def download_new_files():
    # Simulate FTP connection (normally you would connect to a real server)
    try:
        # Uncomment this for real FTP connection
        # ftp = ftplib.FTP(FTP_SERVER)
        # ftp.login(FTP_USER, FTP_PASSWORD)
        # ftp.cwd(FTP_DIRECTORY)
        # files = ftp.nlst()

        # Simulating file listing for now
        files = [
            'MED_DATA_20250425120000.csv',
            'MED_DATA_20250425130000.csv',
            'MED_DATA_20250425140000.csv'
        ]

        processed_files = load_processed_files()

        for file in files:
            if file not in processed_files:
                print(f"Downloading new file: {file}")
                # Uncomment this for real FTP download
                # with open(os.path.join(LOCAL_DOWNLOAD_DIR, file), 'wb') as f:
                #     ftp.retrbinary('RETR ' + file, f.write)
                # For simulation, create dummy local file
                with open(os.path.join(LOCAL_DOWNLOAD_DIR, file), 'w') as f:
                    f.write('Simulated file content')
                save_processed_file(file)
            else:
                print(f"Skipping already processed file: {file}")

        # Uncomment this if using real FTP
        # ftp.quit()

    except Exception as e:
        print(f"FTP connection failed: {e}")

if __name__ == "__main__":
    download_new_files()
    