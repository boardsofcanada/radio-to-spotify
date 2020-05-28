# -*- coding: utf-8 -*-

import time
import config
import sys
from utils import get_current_date
from spotify_authorization import SpotifyAuthorization
from spotify_api import SpotifyAPI
from radio_stations import RadioStations


# authorization
spotify_auth = SpotifyAuthorization(
    config.SPOTIFY_CLIENT_ID,
    config.SPOTIFY_CLIENT_SECRET,
    config.SPOTIFY_REDIRECT_URI,
    config.SPOTIFY_SCOPE
)

if not spotify_auth.main():
    sys.exit("Refresh token could not taken.")

# api
spotify_api_obj = SpotifyAPI(
    config.SPOTIFY_CLIENT_ID,
    config.SPOTIFY_CLIENT_SECRET,
    config.SPOTIFY_USER,
    spotify_auth.refresh_token
)

# radio stations
radio_stations_obj = RadioStations()

#
playlist_date = get_current_date()
playlist_id = False
temporary_added_tracks = []
while True:
    # token
    if spotify_api_obj.is_token_expired():
        spotify_api_obj.refresh_access_token()

    # playlist
    current_date = get_current_date()
    if (not playlist_id) or (playlist_date != current_date):
        playlist_date = current_date
        playlist_name = f'{config.PLAYLIST_NAME} - {playlist_date}'

        playlist_id = spotify_api_obj.is_playlist_exist(playlist_name)
        if not playlist_id:
            playlist_id = spotify_api_obj.create_playlist(playlist_name)

            # clear the added tracks when new playlist created
            temporary_added_tracks.clear()

    # track
    radio_stations_obj.main()

    while not radio_stations_obj.tracks.empty():
        track_name = radio_stations_obj.tracks.get()
        print(track_name)

        if track_name not in temporary_added_tracks:
            track_id = spotify_api_obj.search_track(track_name)
            temporary_added_tracks.append(track_name)

            if track_id:
                spotify_api_obj.add_track_to_playlist(track_id, playlist_id)


    time.sleep(60*3)
