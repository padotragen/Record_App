# module dataprocessing
from flask import abort
import time
import os
import json


# Checks if file is older than the specified time in minutes
# If file does not exsist it will return true
# If minutes are not specified when calling the function, it will default to 120.
def if_file_older_than(file_path, min=120):
    if not os.path.exists(file_path):
        return True

    fmTime = os.path.getmtime(file_path)
    current_time = time.time()

    return (current_time - fmTime) > (min * 60)  # 30 minutes in seconds


# Checks if path exsists, if not create it.
def ensure_filepath(file_path):
    directory = os.path.dirname(file_path)  # Extracts the directory path
    if directory and not os.path.exists(
        directory
    ):  # Creates directory if it doesn't exist
        os.makedirs(directory)


# Function to normalize artist names for sorting
def normalize_artist_name(artist):
    return artist.lower().removeprefix("the ").strip()


# Load vinyl collection from the specified Cached Collection File
def load_collection(DATA_FOLDER, filename):
    file_path = os.path.join(DATA_FOLDER, filename)

    if not os.path.exists(file_path):
        abort(404, description="File not found")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, str):  # If it's a string, parse it again
        data = json.loads(data)

    # print(type(data))
    return data


# Retreive Collection For Discogos User and Write to File
def retrieve_collection(d, file_path):
    # defining identity used against Discog API
    me = d.identity()
    total_collection = {}

    ensure_filepath(file_path)

    for item in me.collection_folders[0].releases:
        total_collection[item.id] = retrieve_releaseInfo(d, item.id)

    json_collection = json.dumps(total_collection, indent=4)

    with open(file_path, "w") as file:
        json.dump(json_collection, file)


# Retrieve Track Info from Discogos and Write to File
def retrieve_trackInfo(DATA_FOLDER, d, releaseID):
    collection_file = f"releases/{releaseID}.json"
    file_path = os.path.join(DATA_FOLDER, collection_file)
    release = d.release(releaseID)
    albumList = []
    for track in release.tracklist:
        trackDict = {
            "Track": track.title,
            "Track Number": track.position,
            "Duration": track.duration,
            "Artists": [artist.name for artist in track.artists],
            "Credits": [credit.name for credit in track.credits],
        }

        albumList.append(trackDict)

    json_collection = json.dumps(albumList, indent=4)
    ensure_filepath(file_path)

    with open(file_path, "w") as file:
        json.dump(json_collection, file)


# Retrieve Release from Discgos
def retrieve_releaseInfo(d, releaseID):
    release = d.release(releaseID)
    imgDict = release.images[0]

    releaseDict = {
        "releaseId": release.id,
        "artist": release.artists[0].name,
        "title": release.title,
        "labels": release.labels[0].name,
        "format": release.formats,
        "year": release.year,
        "genres": release.genres,
        "imageURI": imgDict["uri"],
    }

    return releaseDict


# Retreive the Release Info from Cached Collection File
def load_releaseInfo(releaseID, file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)  # Ensure the JSON is loaded as a dictionary

    try:
        data = json.loads(data)  # In case data is still a string, parse it again
    except TypeError:
        pass  # If it's already a dict, this won't be needed

    # Search for the release by ID
    release_info = data.get(str(releaseID))

    if release_info:
        return release_info
    else:
        abort(404, description=f"No release found with ID {releaseID}")
        # return f"No release found with ID {release_id}"


# Retreive the Track Info from Cached Files
# If the Cached File does not exist, create the Cached File
def load_trackInfo(releaseID, file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        track_info = json.load(file)  # Ensure the JSON is loaded as a dictionary

    try:
        track_info = json.loads(
            track_info
        )  # In case data is still a string, parse it again
    except TypeError:
        pass  # If it's already a dict, this won't be needed

    if track_info:
        return track_info
    else:
        abort(404, description=f"No Track List found with ID {releaseID}")
