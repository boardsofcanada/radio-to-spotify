#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: Batuhan Gürses

import os
import requests
import time
import pytz
from datetime import datetime
import config
import radio_eksen
import spotify_api
import spotify_auth

def file_check():
    """
        Checks the 'authorizon_code.txt' file.
        If the file not exists, returns False.
        If the file exists, returns line of file as list.
    """
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        file = open(path + '/refresh_token.txt', 'r')
        return file.readlines()
    except:
        return False


def access_token_control(headers):
    """
        Checks whether the access token ends.

        Params:
        header -- header of access token
            example -> '{Authorization: Bearer NgCXRK...MzYjw}'

        If access token ends, returns False
    """
    url = 'https://api.spotify.com/v1/me/playlists'
    req = requests.get(url, headers = headers)
    if req.status_code == 200:
        return True
    else:
        return False

auth_header_base64 = spotify_auth.authorization_header_base64(
    config.SPOTIFY_CLIENT_ID,
    config.SPOTIFY_CLIENT_SECRET
    )

radio_timezone = pytz.timezone("Europe/Istanbul") # time zone of Radio Eksen location
date = datetime.now(radio_timezone)
date = datetime.strftime(date,'%d.%m.%y')
playlist_id = ''
access_token = ''
tracks = []

while True:
    # 'current_date' variable is for create playlist if date changes when program is running.
    current_date = datetime.now(radio_timezone)
    current_date = datetime.strftime(current_date,'%d.%m.%y')
    playlist_name = current_date + ' - Radyo Eksen'
    # if code running first time.
    if file_check() == False:
        spotify_auth.request_authorization(
            config.SPOTIFY_CLIENT_ID,
            config.SPOTIFY_REDIRECT_URI,
            config.SPOTIFY_SCOPE
            )
        auth_code = input('Please paste url:\n')
        auth_code = auth_code.split('?code=')[-1]
        # request access and refresh token.
        token = spotify_auth.get_token(
            auth_code,
            config.SPOTIFY_REDIRECT_URI,
            auth_header_base64
            )
        access_token = token[0]
        refresh_token = token[1]
        path = os.path.dirname(os.path.abspath(__file__))
        writer = open(path + '/refresh_token.txt', 'w')
        # only write the refresh token to the file.
        writer.write(refresh_token)
        writer.close()
        time.sleep(2)
        continue
    auth_header_bearer = spotify_api.authorization_header_bearer(access_token)
    token_control = access_token_control(auth_header_bearer)
    # if token expire
    if token_control == False:
        refresh_token = file_check()[0].strip()
        # new access token
        access_token = spotify_auth.refresh_access_token(
            refresh_token,
            auth_header_base64
            )
        continue
    if not playlist_id or current_date != date:
        date = current_date
        playlists = spotify_api.list_playlist(auth_header_bearer)
        # program creates only one new playlist in every day
        # playlist name example --> '13.09.2018 - Radio Eksen'
        # if playlist was created, not create one more.
        for playlist in playlists:
            if playlist[1] == playlist_name:
                playlist_id = playlist[2]
                break
        else:
            # if playlist was not created, creates one new playlist
            playlist_id = spotify_api.create_playlist(
            config.SPOTIFY_USER,
            auth_header_bearer,
            playlist_name
            )
    if tracks == []:
        # this block runs only one time when code starts every
        # for not add songs that played before the program started
        tracks = radio_eksen.radio_eksen()
    else:
        current_tracks = radio_eksen.radio_eksen()
        if current_tracks != tracks:
            to_add_tracks = [track for track in current_tracks if track not in tracks]
            track_id = spotify_api.search_track(to_add_tracks[0], auth_header_bearer)
            if track_id != None: # if track found in spotify, adds to playlist
                spotify_api.add_track_to_playlist(
                    track_id,
                    playlist_id,
                    auth_header_bearer
                    )
            tracks = current_tracks
    time.sleep(60)
