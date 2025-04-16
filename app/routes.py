from flask import render_template, jsonify, request, redirect, url_for
import os
import discogs_client
import app.dpmodule as dp

from app import app
from app.forms import SettingsForm

# Default data folder
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")
DEFAULT_FILE = app.config["DEFAULT_FILE"]
USER_TOKEN = app.config["API_KEY"]

# Discogs Client for wrighwj
d = discogs_client.Client("ExampleApplication/0.1", user_token=USER_TOKEN)


@app.route("/")
def index():
    # return render_template("index.html")
    return redirect(url_for("collection"))


@app.route("/collection")
def collection():
    collection_file = DEFAULT_FILE
    collection_file_path = os.path.join(DATA_FOLDER, collection_file)

    if not os.path.exists(collection_file_path):
        dp.retrieve_collection(d, collection_file_path)
    if dp.if_file_older_than(collection_file_path, 2880):
        dp.retrieve_collection(d, collection_file_path)

    collection = dp.load_collection(DATA_FOLDER, collection_file)

    if not isinstance(collection, dict):
        print("Error: collection is not a dictionary")
        return "Error loading collection", 500

    # Get sorting criteria from the request (default to sorting by artist)
    sort_by = request.args.get("sort", "artist")
    filter_term = request.args.get("filter", "").lower()

    if sort_by == "artist":
        collection = dict(
            sorted(
                collection.items(),
                key=lambda item: dp.normalize_artist_name(item[1]["artist"]),
            )
        )
    elif sort_by == "year":
        collection = dict(
            sorted(collection.items(), key=lambda item: item[1].get("year", 0))
        )  # Default to 0 if year is missing
    elif sort_by == "album":
        collection = dict(
            sorted(
                collection.items(),
                key=lambda item: dp.normalize_artist_name(item[1]["title"]),
            )
        )

    # Apply filtering
    if filter_term:
        collection = {
            key: value
            for key, value in collection.items()
            if filter_term in value["artist"].lower()
            or filter_term in value["title"].lower()
            or filter_term in str(value.get("year", "")).lower()
        }

    return render_template("collection.html", data=collection)


@app.route("/release")
def release():
    releaseID = request.args.get("id", "23314745")

    # Retreive Collection Info Based on the User Token
    # me=d.identity()
    collection_file = DEFAULT_FILE
    collection_file_path = os.path.join(DATA_FOLDER, collection_file)

    if not os.path.exists(collection_file_path):
        dp.retrieve_collection(d, collection_file_path)
    if dp.if_file_older_than(collection_file_path, 2880):
        dp.retrieve_collection(d, collection_file_path)

    # Retrieves Release Info from Collection Cache File
    releaseInfo = dp.load_releaseInfo(releaseID, collection_file_path)

    # Specify Cached Release File
    release_file = f"releases/{releaseID}.json"
    release_file_path = os.path.join(DATA_FOLDER, release_file)

    # Checks to see if the Cached Release File exists. If not generate the Release File.
    if not os.path.exists(release_file_path):
        dp.retrieve_trackInfo(DATA_FOLDER, d, releaseID)

    trackInfo = dp.load_trackInfo(releaseID, release_file_path)

    # print(releaseInfo)

    # print(type(trackInfo))
    return render_template("release.html", album=releaseInfo, tracks=trackInfo)


@app.route("/carousel")
def carousel():
    collection_file = DEFAULT_FILE
    collection_file_path = os.path.join(DATA_FOLDER, collection_file)

    if not os.path.exists(collection_file_path):
        dp.retrieve_collection(d, collection_file_path)
    if dp.if_file_older_than(collection_file_path, 2880):
        dp.retrieve_collection(d, collection_file_path)

    collection = dp.load_collection(DATA_FOLDER, collection_file)

    if not isinstance(collection, dict):
        print("Error: collection is not a dictionary")
        return "Error loading collection", 500

    # Get sorting criteria from the request (default to sorting by artist)
    sort_by = request.args.get("sort", "artist")
    filter_term = request.args.get("filter", "").lower()

    if sort_by == "artist":
        collection = dict(
            sorted(
                collection.items(),
                key=lambda item: dp.normalize_artist_name(item[1]["artist"]),
            )
        )
    elif sort_by == "year":
        collection = dict(
            sorted(collection.items(), key=lambda item: item[1].get("year", 0))
        )  # Default to 0 if year is missing
    elif sort_by == "album":
        collection = dict(
            sorted(
                collection.items(),
                key=lambda item: dp.normalize_artist_name(item[1]["title"]),
            )
        )

    # Apply filtering
    if filter_term:
        collection = {
            key: value
            for key, value in collection.items()
            if filter_term in value["artist"].lower()
            or filter_term in value["title"].lower()
            or filter_term in str(value.get("year", "")).lower()
        }

    return render_template("carousel.html", data=collection)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    collection_file = DEFAULT_FILE
    collection_file_path = os.path.join(DATA_FOLDER, collection_file)

    me = d.identity()

    userProfile = {
        "username": me.username,
        "fullName": me.name,
        "url": me.url,
        "collectionNum": me.num_collection,
    }

    form = SettingsForm()
    if form.validate_on_submit():
        dp.retrieve_collection(d, collection_file_path)
    return render_template("settings.html", form=form, userProfile=userProfile)


@app.route("/api/collection")
def api_collection():
    filename = request.args.get("file", DEFAULT_FILE)
    collection = dp.load_collection(DATA_FOLDER, filename)
    return jsonify(collection)
