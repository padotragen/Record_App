from flask import Flask
from config import Config
import discogs_client

app = Flask(__name__)
app.config.from_object(Config)

#Retrieving the API KEY from the Environment and Generate the DEFAULT_FILE name
USER_TOKEN = app.config['API_KEY']

if not USER_TOKEN:
    raise ValueError("API Key is missing. Set the 'API_KEY' environment variable.")

d = discogs_client.Client('ExampleApplication/0.1', user_token=USER_TOKEN)
me=d.identity()
app.config['DEFAULT_FILE'] = f"{me.id}.json"

from app import routes