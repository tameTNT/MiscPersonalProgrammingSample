import spotipy  # Gets a playlist's songs
import spotipy.util as util  # Gets authentication token from spotify dev
from statistics import mean

print("[py] Getting auth token...")
token = util.prompt_for_user_token("luca_py", "playlist-read-private", redirect_uri="http://localhost:8888/callback/")
sp = spotipy.Spotify(auth=token)


def get_tracks_from_playlist(playlist_uri):
    def iterate_over_track_list(input_song_list, output_song_list):
        for i, item in enumerate(input_song_list['items']):
            track = item['track']
            output_song_list.append(track['id'])

    print("[py] Getting playlist track list...")
    if "spotify:playlist:" in playlist_uri:
        playlist_uri = playlist_uri[17:]  # removes "spotify:playlist:" from start of uri
    playlist_songs = sp.playlist(playlist_uri)['tracks']

    final_song_list = []
    iterate_over_track_list(playlist_songs, final_song_list)
    while playlist_songs['next']:  # needed for 'paged' playlists with over 100 songs
        iterate_over_track_list(sp.next(playlist_songs), final_song_list)
        prev_offset = int(playlist_songs['next'].split("?offset=")[1].split("&")[0])
        new_offset = prev_offset + 100
        if new_offset < playlist_songs["total"]:
            playlist_songs['next'] = playlist_songs['next'].replace(f"?offset={prev_offset}", f"?offset={new_offset}")
        else:
            playlist_songs['next'] = None

    return final_song_list


def get_loudness_mean(playlist_uri):
    tracks = get_tracks_from_playlist(uri)
    num = len(tracks)
    loudness_list = list()
    print(f"Starting playlist {uri}", end="\n")
    for i, song_id in enumerate(tracks):
        print(f"{i/num * 100:.2f}% on playlist {uri}", end="\r")
        a = sp.audio_analysis(song_id)
        loudness_list.append(float(a['track']['loudness']))
    print(f"100.00% on playlist {uri}")

    return mean(loudness_list)


playlist_loudness = dict()
uri_list = ["67lpvmy4JD7MwfaLr9dD15", "4QpNckPr2VuLoLLuIqvVHK", "7fkVQLgW8TfboWD7pXMSAC"]  # Luca, Joel, Luke
for uri in uri_list:
    playlist_loudness[uri] = get_loudness_mean(uri)

print(playlist_loudness)
