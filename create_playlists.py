from sys import argv, exit
import os
import json
import requests
import time

if len(argv) > 1 and argv[1]:
    pass
else:
    print('\nCommand usage:\npython3 create_playlist.py yourplaylist_itunes-version.csv\nMore info at https://github.com/therealmarius/Spotify-2-AppleMusic')
    exit()

token = os.getenv("APPLE_MUSIC_BEARER_TOKEN", None)
media_user_token = os.getenv("APPLE_MUSIC_MEDIA_USER_TOKEN", None)
cookies = os.getenv("APPLE_MUSIC_COOKIES", None)

if not token:
    token = input("\nPlease enter your Apple Music Authorization (Bearer token):\n")
if not media_user_token:
    media_user_token = input("\nPlease enter your media user token:\n")
if not cookies:
    cookies = input("\nPlease enter your cookies:\n")

with open(argv[1]) as hack:
    pass

playlist_base_name = argv[1][:len(argv[1])-len('_itunes-version.csv')]
playlist_mapping = f'{playlist_base_name}_itunes-id.txt'
try:
    with open(playlist_mapping, 'r') as mapping_file:
        playlist_id = mapping_file.read()
        if playlist_id:
            # skip if we already have this ID
            exit(0)
except FileNotFoundError:
    pass

with requests.Session() as s:
    playlist_name = playlist_base_name.replace('_', ' ').strip()
    data = {"attributes":{"name":playlist_name},"relationships":{}}
    content_length = len(json.dumps(data, separators=(',', ':')))
    s.headers.update({"Authorization": f"{token}",
                    "media-user-token": f"{media_user_token}",
                    "Cookie": f"{cookies}",
                    "Host": "amp-api.music.apple.com",
                    "Accept-Encoding":"gzip, deflate, br",
                    "Referer": "https://music.apple.com/",
                    "Origin": "https://music.apple.com",
                    "Content-Length": f"{content_length}",
                    "Connection": "keep-alive",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-site",
                    "TE": "trailers"})

    request = s.post(f"https://amp-api.music.apple.com/v1/me/library/playlists", json=data)
    if requests.codes.ok:
        resp = request.json()
        playlist_id = resp['data'][0]['id']
        print(f"Created playlist, {playlist_name}: {playlist_id}")
        with open(playlist_mapping, 'w', encoding='utf-8') as mapping_file:
            mapping_file.write(playlist_id)
        time.sleep(5)
    else:
        print(f"Error {request.status_code} creating playlist, {playlist_name}!")

# Developped by @therealmarius on GitHub
# Based on the work of @simonschellaert on GitHub
# Github project page: https://github.com/therealmarius/Spotify-2-AppleMusic
