import spotipy  # gets playlist's songs
import spotipy.util as util  # gets auth token from spotify dev
import json


def query_tracks(tracks, l):
    for item in tracks['items']:
        track = item['track']
        if input(f"'{track['name']}' by '{track['artists'][0]['name']}' on '{track['album']['name'][:50]}'... ").lower() == "y":
            l.append(track["id"])


def return_playlist_by_uri(playlists, qu_type):
    target_uri = input(f"Enter {qu_type} playlist uri:")
    i = 0
    try:
        while target_uri != playlists[i]["uri"]:
            i += 1
    except IndexError:
        raise Exception("Personal public playlist with that uri not found in user's library")
    return playlists[i]["id"]


print("Getting auth token...")
token = util.prompt_for_user_token("lucahuelle", 'playlist-modify-public', client_id='',
                                   client_secret='', redirect_uri='http://localhost/')
sp = spotipy.Spotify(auth=token)

user_playlists = sp.user_playlists("lucahuelle")["items"]

starting_playlist_id = return_playlist_by_uri(user_playlists, "starting")
destination_playlist_id = return_playlist_by_uri(user_playlists, "destination")

results = sp.playlist(starting_playlist_id, fields="tracks,next")
tracks = results['tracks']

log_bool = (input("Log these inputs? y/n: ").lower() == "y")
if log_bool:
    print("Logging responses...")

print("Copy track to destination playlist? Enter y/n per track.")
track_ids_to_add = list()
query_tracks(tracks, track_ids_to_add)
while tracks['next']:
    tracks = sp.next(tracks)
    query_tracks(tracks, track_ids_to_add)

if log_bool:
    with open("track_add_choice_log.json", "w+") as fobj:
        json.dump(track_ids_to_add, fobj)
        fobj.close()

if input(f"Add {len(track_ids_to_add)} tracks to playlist with uri '{destination_playlist_id}'? y/n: ").lower() == "y":
    sp.user_playlist_add_tracks("lucahuelle", destination_playlist_id, track_ids_to_add)
