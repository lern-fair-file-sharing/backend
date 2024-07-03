import os
import requests
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import json

f = open("./example-tags/tag-init.json", "r")
json_data = json.load(f)

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

def get_folder_content(directory):
    headers = {
        "Content-Type": "text/plain",
    }
    body = '''<?xml version="1.0" encoding="UTF-8"?>
    <d:propfind xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
        <d:prop>
            <oc:fileid />
        </d:prop>
    </d:propfind>'''

    response = requests.request("PROPFIND", WEBDAV_URL+directory, headers=headers, data=body, auth=auth)

    fileID = ""

    if response.status_code == 207:
        root = ET.fromstring(response.content)
        for response_elem in root.findall('{DAV:}response'):
            path = response_elem.find('{DAV:}href').text

            if path.endswith("/"):
                print("We need files only")
            else:
                fileID = response_elem.find('{DAV:}propstat/{DAV:}prop/{http://owncloud.org/ns}fileid').text
    else:
        print("Error fetching folder content:", response.status_code, response.text)

    return fileID

# Function to upload a file
def upload_file(directory_path, file_name, file_path):
    with open(file_path, "rb") as file_content:
        url = WEBDAV_URL + directory_path + "/" + file_name
        response = requests.put(url, data=file_content, auth=auth)
        if response.status_code in (201, 204):
            print(f"File uploaded: {directory_path}/{file_name}")
            fileID = get_folder_content("/"+directory_path+"/"+file_name)
            if fileID:
                
                systemTags = get_all_system_tags()
                for tag in json_data['Existing Tags']:
                    # if the tag is in the directory path string, assign the tag
                    if tag in directory_path:
                        for systemTag in systemTags:
                            if systemTag['tagName'] == tag:
                                if not assign_system_tag(fileID, systemTag):
                                    print("Failed to assign tag.")
                for tag in json_data['Existing Users']:
                    if tag.lower() in file_name:
                        for systemTag in systemTags:
                            if systemTag['tagName'] == tag:
                                if not assign_system_tag(fileID, systemTag):
                                    print("Failed to assign tag.")
            else:
                print("Error finding file")
        else:
            print(f"Error uploading file: {directory_path}/{file_name}")



# Function to get all system tags
def get_all_system_tags():
    headers = {
        "Content-Type": "text/plain",
    }
    body = '''<?xml version="1.0"?>
<d:propfind xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns">
    <d:prop>
        <oc:id />
        <oc:display-name />
        <oc:user-visible />
        <oc:user-assignable />
        <oc:can-assign />
    </d:prop>
</d:propfind>'''

    response = requests.request("PROPFIND", f"{NEXTCLOUD_URL}/remote.php/dav/systemtags/", headers=headers, data=body, auth=auth)

    if response.status_code == 207:
        tags = []
        root = ET.fromstring(response.content)
        for response_elem in root.findall('{DAV:}response'):
            prop = response_elem.find('{DAV:}propstat/{DAV:}prop')
            tag_id = prop.find('{http://owncloud.org/ns}id').text
            tag_name = prop.find('{http://owncloud.org/ns}display-name').text
            if tag_name:
                tags.append({'tagName': tag_name, 'tagID': int(tag_id)})
        return tags
    else:
        print("Failed to get tags:", response.status_code, response.text)

# Function to create a system tag
def create_system_tag(tag_name):
    headers = {
        "Content-Type": "application/json",
    }
    body = {
        "userVisible": True,
        "userAssignable": True,
        "canAssign": True,
        "name": tag_name
    }
    response = requests.post(f"{NEXTCLOUD_URL}/remote.php/dav/systemtags/", headers=headers, json=body, auth=auth)

    if response.status_code in [201, 204]:
        print(f"Tag created: {tag_name}")
    else:
        print("Failed to create tag:", response.status_code, response.text)

# Function to assign a system tag
def assign_system_tag(file_id, tag):
    headers = {
        "Content-Type": "application/json",
    }
    body = {
        "id": str(tag['tagID']),
        "userVisible": True,
        "userAssignable": True,
        "canAssign": True,
        "name": tag['tagName']
    }
    response = requests.put(f"{NEXTCLOUD_URL}/remote.php/dav/systemtags-relations/files/{file_id}/{tag['tagID']}", headers=headers, json=body, auth=auth)

    if response.status_code in [201, 204]:
        print(f"Tag {tag['tagName']} assigned to file ID {file_id}")
        return True
    else:
        print("Failed to assign tag:", response.status_code, response.text)
        return False


delete_all_files()
for tag in json_data['Existing Tags']:
    create_system_tag(tag)
for tag in json_data['Existing Users']:
    create_system_tag(tag)
for tag in json_data['File Types']:
    create_system_tag(tag)
print(get_all_system_tags())

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


f.close()