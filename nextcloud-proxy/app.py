from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
from xml.etree import ElementTree as ET
from config import NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD

app = Flask(__name__)

auth = HTTPBasicAuth(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD)

# Helper function to ensure the URL is correctly formatted
def format_url(path):
    if not NEXTCLOUD_URL.endswith("/"):
        base_url = NEXTCLOUD_URL + "/"
    else:
        base_url = NEXTCLOUD_URL
    
    if path.startswith("/"):
        path = path[1:]
    
    return base_url + path

# Helper function to parse XML response
def parse_xml_response(xml_content):
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

# Route to fetch a folder
@app.route("/fetch-folder", methods=["GET"])
def fetch_folder():
    folder_path = request.args.get("path", "")
    url = format_url(folder_path)
    headers = {"Depth": "1"}
    response = requests.request("PROPFIND", url, auth=auth, headers=headers)

    if response.status_code == 207:
        items = parse_xml_response(response.content)
        return jsonify(items), 200
    else:
        return jsonify({"error": "Failed to fetch folder"}), response.status_code

# Route to fetch the last 20 modified/added files from a folder
@app.route("/fetch-recent-files", methods=["GET"])
def fetch_recent_files():
    folder_path = request.args.get("path", "")
    url = format_url(folder_path)
    headers = {"Depth": "1"}
    response = requests.request("PROPFIND", url, auth=auth, headers=headers)

    if response.status_code == 207:
        files = []
        tree = ET.fromstring(response.content)
        for response in tree.findall(".//{DAV:}response"):
            href = response.find("{DAV:}href").text
            last_modified = response.find(".//{DAV:}getlastmodified")
            files.append({"href": href, "last_modified": last_modified.text if last_modified is not None else ""})

        sorted_files = sorted(files, key=lambda x: x["last_modified"], reverse=True)[:20]
        return jsonify(sorted_files)
    else:
        return jsonify({"error": "Failed to fetch recent files"}), response.status_code

# Route to upload files
@app.route("/upload", methods=["POST"])
def upload_files():
    folder_path = request.form.get("path", "")
    files = request.files.getlist("files")

    for file in files:
        url = format_url(folder_path + "/" + file.filename)
        response = requests.put(url, data=file.read(), auth=auth)
        if response.status_code not in (201, 204):
            return jsonify({"error": f"Failed to upload {file.filename}"}), response.status_code

    return jsonify({"message": "Files uploaded successfully"}), 200


def init_admin_user():
    url = "http://localhost:8080/index.php"

    payload = {
        "install": "true",
        "adminlogin": NEXTCLOUD_USERNAME,
        "adminpass": NEXTCLOUD_PASSWORD,
        "directory": "/var/www/html",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        print("Nextcloud setup completed successfully!")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    try:
        init_admin_user()
    except Exception as e:
        print(str(e))
    finally:
        app.run(debug=True)
