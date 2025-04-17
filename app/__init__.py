from flask import Flask
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os
import discogs_client

app = Flask(__name__)
app.config.from_object(Config)

if not app.debug:
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/RecordCollection.log", maxBytes=10240, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("Record Collection startup")


# Retrieving the API KEY from the Environment and Generate the DEFAULT_FILE name
USER_TOKEN = app.config["API_KEY"]

if not USER_TOKEN:
    app.logger.error("API Key is missing. Set the 'API_KEY' environment variable.")
    raise ValueError("API Key is missing. Set the 'API_KEY' environment variable.")

d = discogs_client.Client("ExampleApplication/0.1", user_token=USER_TOKEN)
me = d.identity()
app.config["DEFAULT_FILE"] = f"{me.id}.json"

from app import dpmodule, routes, errors
