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

# Run this only if the script is executed directly
if __name__ == "__main__":
    print("Generated UUID:", get_guid())
