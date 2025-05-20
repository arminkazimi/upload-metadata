import requests
import sys
import json
from decouple import config
# from decouple import RepositoryEnv
# config = Config(RepositoryEnv("path/to/env_file"))
# Configuration for server --Ari--
base_url = "http://localhost:8000"

def send_metadata_json_to_server(base_url, project_id, json_data):
    url = f"{base_url}/api/projects/{project_id}/metadata/"

    headers = {
        # Add authentication if required
        "Authorization": f"Api-Key {config('API_KEY', default=None)}"
    }
    print(headers)
    # Partial update data - only include fields you want to update
    data = {
        "status": "success"  # Optional: Only include fields to update
    }

    files = {
        "metadata_json": ('data.json', json_data, 'application/json')
    }

    try:
        # Send PATCH request
        response = requests.patch(
            url,
            data=data,
            files=files,
            headers=headers
        )
        response.raise_for_status()

        print(f"Status Code: {response.status_code}")
        print("Partially Updated MetaData:")
        print(response.json())

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        print(f"Response content: {err.response.text}")
    except Exception as err:
        print(f"Error: {err}")
    finally:
        if 'metadata_json' in files:
            # Check if the object has a 'close' method (indicating it's a file-like object)
            if hasattr(files["metadata_json"], 'close'):
                files["metadata_json"].close()
# Configuration for server --Ari-- --END--


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sendFile.py <json_file_path>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    project_file_id = json_file_path.split('\\')[-1].split('.')[0]  # Extract ID from filename
    print(project_file_id)
    try:
        with open(json_file_path, 'r') as f:
            json_data = f.read()
        
        send_metadata_json_to_server(base_url, project_file_id, json_data)
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file_path}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON file '{json_file_path}'")
        sys.exit(1)
    except Exception as err:
        print(f"Error: {err}")

