import os
import requests
from dotenv import load_dotenv

# Load the credentials from the .env file
load_dotenv()

NEXTCLOUD_URL = "http://localhost:8080"
USERNAME = os.getenv("NCUSR")
PASSWORD = os.getenv("NCPW")

# Debugging statements to ensure variables are loaded correctly
print(f"Nextcloud URL: {NEXTCLOUD_URL}")
print(f"Username: {USERNAME}")
print(f"Password: {PASSWORD}")

# Ensure the credentials are correctly loaded
if not USERNAME or not PASSWORD:
    raise ValueError("Username or password not found. Check your .env file.")

# WebDAV URL
WEBDAV_URL = f"{NEXTCLOUD_URL}/remote.php/dav/files/{USERNAME}/"

# Basic auth for WebDAV
auth = (USERNAME, PASSWORD)

# Function to delete all files in the Nextcloud root directory
def delete_all_files():
    response = requests.request("PROPFIND", WEBDAV_URL, auth=auth)
    if response.status_code == 207:
        items = response.text.split("<d:href>")
        for item in items[1:]:
            href = item.split("</d:href>")[0]
            if not WEBDAV_URL.endswith(href):
                requests.delete(f"{NEXTCLOUD_URL}{href}", auth=auth)
                print(f"Deleted: {href}")
    else:
        print("Error fetching files")

# Function to create a directory
def create_directory(directory_path):
    url = WEBDAV_URL + directory_path
    response = requests.request("MKCOL", url, auth=auth)
    if response.status_code in (201, 405):
        print(f"Directory created: {directory_path}")
    else:
        print(f"Error creating directory: {directory_path}")

# Function to upload a file
def upload_file(directory_path, file_name, file_path):
    with open(file_path, "rb") as file_content:
        url = WEBDAV_URL + directory_path + "/" + file_name
        response = requests.put(url, data=file_content, auth=auth)
        if response.status_code in (201, 204):
            print(f"File uploaded: {directory_path}/{file_name}")
        else:
            print(f"Error uploading file: {directory_path}/{file_name}")

# Delete all files in the root directory
delete_all_files()

# Path to the local directory structure to replicate
local_base_path = "./example-folder-structure"

# Traverse the local directory structure
for root, dirs, files in os.walk(local_base_path):
    relative_path = os.path.relpath(root, local_base_path)
    nextcloud_path = "" if relative_path == "." else relative_path.replace("\\", "/")
    
    # Create directories in Nextcloud
    for directory in dirs:
        create_directory(os.path.join(nextcloud_path, directory))
    
    # Upload files to Nextcloud
    for file in files:
        file_path = os.path.join(root, file)
        upload_file(nextcloud_path, file, file_path)
