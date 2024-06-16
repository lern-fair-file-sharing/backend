from xml.etree import ElementTree as ET
import requests
from requests.auth import HTTPBasicAuth
import time
import sys


def parse_xml_response(xml_content: str) -> dict:
    tree = ET.fromstring(xml_content)
    items = []
    for response in tree.findall(".//{DAV:}response"):
        href = response.find("{DAV:}href").text
        displayname = response.find(".//{DAV:}displayname")
        is_collection = response.find(".//{DAV:}resourcetype/{DAV:}collection") is not None
        last_modified = response.find(".//{DAV:}getlastmodified")

        items.append({
            "href": href,
            "displayname": displayname.text if displayname is not None else "",
            "is_collection": is_collection,
            "last_modified": last_modified.text if last_modified is not None else ""
        })
    return items


def format_url(path: str, url: str) -> str:
    if not url.endswith("/"):
        base_url = url + "/"
    else:
        base_url = url
    
    if path.startswith("/"):
        path = path[1:]
    
    return base_url + path



def init_admin_user(username: str, password: str, url: str) -> None:
    payload = {
        "install": "true",
        "adminlogin": username,
        "adminpass": password,
        "directory": "/var/www/html",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(f"{url}/index.php", data=payload, headers=headers)

    if response.status_code == 200:
        print(response.content)
        print("Successfully created admin user.")
    else:
        raise Exception(f"Error {response.status_code}:\n{response.text}")


def initialize_folders(username: str, password: str, url: str):
    folders = [
        "Folder1",
        "Folder2",
        "Folder3",
        "Folder1/SubFolder"
    ]
    
    auth = HTTPBasicAuth(username, password)
    
    for folder in folders:
        print(f"Initializing folder files/{username}/{folder}...")
        response = requests.request(
            "MKCOL",
            f"{url}/remote.php/dav/files/{username}/{folder}",
            auth=auth
        )
        
        if response.status_code == 201:
            print("Success.")
        elif response.status_code == 405:
            print(f"Folder '{folder}' already exists.")
        else:
            print(f"Failed to create folder '{folder}'. Status code: {response.status_code}, {response.cookies}")



def initialize_instance(username: str, password: str, url: str) -> None:
    max_tries, tries = 0, 50
    success = False
    while not success:
        time.sleep(2)
        try:
            init_admin_user(username, password, url)
            success = True
        except:
            pass

        if tries == max_tries:
            sys.exit(1)

        tries += 1

    initialize_folders(username, password, url)
