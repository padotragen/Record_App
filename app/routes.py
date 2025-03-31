from flask import Flask, render_template, jsonify, request, abort, redirect, url_for
import json
import os
import discogs_client
import time
from app import app

# Default data folder
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")
DEFAULT_FILE = app.config['DEFAULT_FILE']
USER_TOKEN = app.config['API_KEY']

# Discogs Client for wrighwj
d = discogs_client.Client('ExampleApplication/0.1', user_token=USER_TOKEN)

# Checks if file is older than the specified time in minutes
# If file does not exsist it will return true
# If minutes are not specified when calling the function, it will default to 30.
def if_file_older_than(file_path, min=120):

    if not os.path.exists(file_path):
        return True

    fmTime = os.path.getmtime(file_path)
    current_time = time.time()

    return (current_time - fmTime) > (min * 60) # 30 minutes in seconds

# Checks if path exsists, if not create it.
def ensure_filepath(file_path):
    directory = os.path.dirname(file_path)  # Extracts the directory path
    if directory and not os.path.exists(directory):  # Creates directory if it doesn't exist
        os.makedirs(directory)

# Function to normalize artist names for sorting
def normalize_artist_name(artist):
    return artist.lower().removeprefix('the ').strip()

# Load vinyl collection from the specified Cached Collection File
def load_collection(filename):
    file_path = os.path.join(DATA_FOLDER, filename)
    
    if not os.path.exists(file_path):
        abort(404, description="File not found")
    
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    
    if isinstance(data, str):  # If it's a string, parse it again
        data = json.loads(data)

    #print(type(data))
    return data

# Retreive Collection For Discogos User and Write to File
def retrieve_collection(d, file_path):
    #defining identity used against Discog API
    me=d.identity()
    total_collection={}

    for item in me.collection_folders[0].releases:
        total_collection[item.id]=retrieve_releaseInfo(d, item.id)
    
    json_collection = json.dumps(total_collection, indent= 4)

    with open(file_path, "w") as file:
        json.dump(json_collection, file)

# Retrieve Track Info from Discogos and Write to File
def retrieve_trackInfo(d, releaseID):
    collection_file = f"releases/{releaseID}.json"
    file_path = os.path.join(DATA_FOLDER, collection_file)
    release = d.release(releaseID)
    albumList = []
    for track in release.tracklist:
        trackDict ={
            "Track" : track.title,
            "Track Number" : track.position,
            "Duration" : track.duration,
            "Artists" : [artist.name for artist in track.artists],
            "Credits" : [credit.name for credit in track.credits]
        }

        albumList.append(trackDict)
    
    json_collection = json.dumps(albumList, indent= 4)
    ensure_filepath(file_path)

    with open(file_path, "w") as file:
        json.dump(json_collection, file)

# Retrieve Release from Discgos
def retrieve_releaseInfo(d, releaseID):
    release = d.release(releaseID)
    imgDict = release.images[0]

    releaseDict = {
        "releaseId" : release.id,
        "artist" : release.artists[0].name,
        "title" : release.title,
        "labels" : release.labels[0].name,
        "format" : release.formats,
        "year" : release.year,
        "genres" : release.genres,
        "imageURI" : imgDict["uri"]
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
        #return f"No release found with ID {release_id}"

# Retreive the Track Info from Cached Files
# If the Cached File does not exist, create the Cached File 
def load_trackInfo(releaseID, file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        track_info = json.load(file)  # Ensure the JSON is loaded as a dictionary
    
    try:
        track_info = json.loads(track_info)  # In case data is still a string, parse it again
    except TypeError:
        pass  # If it's already a dict, this won't be needed
    

    if track_info:
        return track_info
    else:
        abort(404, description=f"No Track List found with ID {releaseID}")


@app.route("/")
def index():
    #return render_template("index.html")
    return redirect(url_for('collection'))

@app.route("/collection")
def collection():
    collection_file = DEFAULT_FILE
    collection_file_path  = os.path.join(DATA_FOLDER, collection_file)

    if not os.path.exists(collection_file_path ):
        retrieve_collection(d, collection_file_path )
    if if_file_older_than(collection_file_path ):
        retrieve_collection(d,collection_file_path )

    collection = load_collection(collection_file)

    if not isinstance(collection, dict):
        print("Error: collection is not a dictionary")
        return "Error loading collection", 500
    
    # Get sorting criteria from the request (default to sorting by artist)
    sort_by = request.args.get("sort", "artist")
    filter_term = request.args.get("filter", "").lower()

    if sort_by == "artist":
        collection = dict(sorted(collection.items(), key=lambda item: normalize_artist_name(item[1]['artist'])))
    elif sort_by == "year":
        collection = dict(sorted(collection.items(), key=lambda item: item[1].get('year', 0)))  # Default to 0 if year is missing
    elif sort_by == "album":
        collection = dict(sorted(collection.items(), key=lambda item: normalize_artist_name(item[1]['title'])))
    
    # Apply filtering
    if filter_term:
        collection = {key: value for key, value in collection.items() if filter_term in value['artist'].lower() or filter_term in value['title'].lower() or filter_term in str(value.get('year', '')).lower()}


    return render_template("collection.html", data=collection)

@app.route("/release")
def release():
    releaseID = request.args.get("id", "23314745")

    # Retreive Collection Info Based on the User Token
    me=d.identity()
    collection_file = DEFAULT_FILE
    collection_file_path = os.path.join(DATA_FOLDER, collection_file)

    if not os.path.exists(collection_file_path ):
        retrieve_collection(d, collection_file_path )
    if if_file_older_than(collection_file_path ):
        retrieve_collection(d,collection_file_path )

    # Retrieves Release Info from Collection Cache File
    releaseInfo = load_releaseInfo(releaseID, collection_file_path)

    # Specify Cached Release File
    release_file = f"releases/{releaseID}.json"
    release_file_path = os.path.join(DATA_FOLDER, release_file)

    # Checks to see if the Cached Release File exists. If not generate the Release File.
    if not os.path.exists(release_file_path):
        retrieve_trackInfo(d, releaseID)
    
    trackInfo = load_trackInfo(releaseID, release_file_path)
    
    #print(releaseInfo)

    #print(type(trackInfo))
    return render_template("release.html", album=releaseInfo, tracks=trackInfo)

@app.route("/carousel")
def carousel():
    collection_file = DEFAULT_FILE
    collection_file_path  = os.path.join(DATA_FOLDER, collection_file)

    if not os.path.exists(collection_file_path ):
        retrieve_collection(d, collection_file_path )
    if if_file_older_than(collection_file_path ):
        retrieve_collection(d,collection_file_path )

    collection = load_collection(collection_file)

    if not isinstance(collection, dict):
        print("Error: collection is not a dictionary")
        return "Error loading collection", 500
    
    # Get sorting criteria from the request (default to sorting by artist)
    sort_by = request.args.get("sort", "artist")
    filter_term = request.args.get("filter", "").lower()

    if sort_by == "artist":
        collection = dict(sorted(collection.items(), key=lambda item: normalize_artist_name(item[1]['artist'])))
    elif sort_by == "year":
        collection = dict(sorted(collection.items(), key=lambda item: item[1].get('year', 0)))  # Default to 0 if year is missing
    elif sort_by == "album":
        collection = dict(sorted(collection.items(), key=lambda item: normalize_artist_name(item[1]['title'])))
    
    # Apply filtering
    if filter_term:
        collection = {key: value for key, value in collection.items() if filter_term in value['artist'].lower() or filter_term in value['title'].lower() or filter_term in str(value.get('year', '')).lower()}


    return render_template("carousel.html", data=collection)


@app.route("/api/collection")
def api_collection():
    filename = request.args.get("file", DEFAULT_FILE)
    collection = load_collection(filename)
    return jsonify(collection)