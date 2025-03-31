import discogs_client
import json
import os


d = discogs_client.Client('ExampleApplication/0.1', user_token="djInylZRGiUQdoWQVJTSNWJZHSWycQNfcBlOPIkD")
me=d.identity()

print(me.id)

# Load JSON data
file_path = "/Users/w.wrightg/Repos/Record_App/app/data/25404341.json"

def retrieve_releaseInfo(d, releaseId):
    release = d.release(releaseId)
    imgDict = release.images[0]

    releaseDict = {
        "releaseId" : release.id,
        "artist" : release.artists[0].name,
        "title" : release.title,
        "lables" : release.labels[0].name,
        "format" : release.formats,
        "year" : release.year,
        "genres" : release.genres,
        "imageURI" : imgDict["uri"]
    }

    return releaseDict

#Retreive the Release Info from Cached Files
def get_releaseInfo_Export(release_id, file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)  # Ensure the JSON is loaded as a dictionary
    
    try:
        data = json.loads(data)  # In case data is still a string, parse it again
    except TypeError:
        pass  # If it's already a dict, this won't be needed

    # Search for the release by ID
    release_info = data.get(str(release_id))
    
    if release_info:
        return release_info
    else:
        #abort(404, description=f"No release found with ID {release_id}")
        return f"No release found with ID {release_id}"

def retrieve_track_info(d, releaseId):
    #collection_file = f"releases/{releaseId}.json"
    #file_path = os.path.join(DATA_FOLDER, collection_file)
    release = d.release(releaseId)
    albumList = []
    
    for track in release.tracklist:
        print(type(track.artists))

        trackDict ={
            "Track" : track.title,
            "Track Number" : track.position,
            "Duration" : track.duration,
            "Artists" : [artist.name for artist in track.artists],
            "Credits" : [credit.name for credit in track.credits]
        }

        albumList.append(trackDict)

    #print(albumList)

    json_collection = json.dumps(albumList)

    file_name = f"{releaseId}.json"
    file_path = "/Users/w.wrightg/Repos/Record_App/app/data/releases/"+file_name
    with open(file_path, "w") as file:
        json.dump(json_collection, file)


releaseID = 11498676
#releaseInfo = d.release(releaseID)
#retrieve_track_info(d, releaseID)

releaseInfo = get_releaseInfo_Export(releaseID, file_path)

#print(releaseInfo)

