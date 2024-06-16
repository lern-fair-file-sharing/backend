from flask import Flask
from routes import nextcloud_routes
from utils import initialize_instance
import logging
from config import NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD, NEXTCLOUD_URL

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.register_blueprint(nextcloud_routes)

initialize_instance(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD, url=NEXTCLOUD_URL)

if __name__ == "__main__":
    app.run()
