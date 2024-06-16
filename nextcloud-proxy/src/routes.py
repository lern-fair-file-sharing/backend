from flask import Blueprint, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
from xml.etree import ElementTree as ET
from config import NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD
from utils import format_url, parse_xml_response

nextcloud_routes = Blueprint("nextcloud", __name__)


@nextcloud_routes.route("/fetch-folder", methods=["GET"])
def fetch_folder():
    auth = HTTPBasicAuth(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD)

    folder_path = request.args.get("path", "")
    url = format_url(folder_path, f"{NEXTCLOUD_URL}/remote.php/webdav/")
    headers = {"Depth": "1"}
    response = requests.request("PROPFIND", url, auth=auth, headers=headers)

    if response.status_code == 207:
        items = parse_xml_response(response.content)
        return jsonify(items), 200
    else:
        return jsonify({"error": "Failed to fetch folder"}), response.status_code


@nextcloud_routes.route("/fetch-recent-files", methods=["GET"])
def fetch_recent_files():
    auth = HTTPBasicAuth(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD)

    folder_path = request.args.get("path", "")
    url = format_url(folder_path, f"{NEXTCLOUD_URL}/remote.php/webdav/")
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
@nextcloud_routes.route("/upload", methods=["POST"])
def upload_files():
    auth = HTTPBasicAuth(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD)

    folder_path = request.form.get("path", "")
    files = request.files.getlist("files")

    for file in files:
        url = format_url(f"{folder_path}/{file.filename}", f"{NEXTCLOUD_URL}/remote.php/webdav/")
        response = requests.put(url, data=file.read(), auth=auth)
        if response.status_code not in (201, 204):
            return jsonify({"error": f"Failed to upload {file.filename}"}), response.status_code

    return jsonify({"message": "Files uploaded successfully"}), 200

