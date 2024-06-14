import os
from dotenv import load_dotenv

load_dotenv()

NEXTCLOUD_URL = "http://localhost:8080/remote.php/webdav/"
NEXTCLOUD_USERNAME = os.getenv("NCUSR")
NEXTCLOUD_PASSWORD = os.getenv("NCPW")