import os
from dotenv import load_dotenv

load_dotenv()

NEXTCLOUD_URL = f"http://{os.getenv('NCHOST')}:{os.getenv('NCPRT')}"
NEXTCLOUD_USERNAME = os.getenv("NCUSR")
NEXTCLOUD_PASSWORD = os.getenv("NCPW")