#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: Batuhan Gürses

import urllib.parse
import requests
import json
import spotify_auth
import config


def authorization_header_bearer(access_token):
    return {'Authorization': 'Bearer ' + access_token}


def search_track(keyw, header):
    """
        Search the uri of track according to the given word.
        Only retrieves first result of the search.

        Params:
        keyw -- search query keyword
            example -> 'Rammstein Mein Teil'
        header -- header of access token
            example -> '{Authorization: Bearer NgCXRK...MzYjw}'

        If track is found, returns the uri.
    """
    url = 'https://api.spotify.com/v1/search?'
    query_params = {
        'q': keyw,
        'type': 'track',
        }
    url = url + urllib.parse.urlencode(query_params)
    req = requests.get(url, headers=header)
    items = req.json()['tracks']['items']
    if req.status_code == 200:
        if items != []:
            return items[0]['uri']
        else:
            return None
    else:
        return None


def add_track_to_playlist(uri, playlist_id, header):
    """
        Adds track to given playlist id.

        Params:
            uri -- uri of track.
                example --> 'spotify:track:0h0smRHEjrkSFUhNWQh8SR'
            playlist_id -- id of the playlist to which the song will be added.
                        The owner of playlist must be the user in config.py
            header -- header of access token
                example -> '{Authorization: Bearer NgCXRK...MzYjw}'

        If the song is successfully added, returns True
    """
    url = 'https://api.spotify.com/v1/playlists/' + str(playlist_id) + '/tracks?uris=' + uri
    req = requests.post(url, headers=header)
    if req.status_code == 201:
        return True
    else:
        return None


def list_playlist(header):
    """
        List playlists of the given user in config.py

        Params:
            header -- header of access token
                example -> '{Authorization: Bearer NgCXRK...MzYjw}'

        If user has playlist(s), returns details of its.
            example -> [[1, '// G*D', '73hUC4Cy5yTJzirc92YkLM'],[...],]
    """
    url = 'https://api.spotify.com/v1/me/playlists'
    req = requests.get(url, headers=header)
    counter = 0
    items = req.json()
    playlists = []
    if req.status_code == 200:
        if items['items'] != []:
            for x in items['items']:
                counter += 1
                playlists.append([counter, x['name'], x['id']])
            return(playlists)
        else:
            return None
    else:
        return None


def create_playlist(user_id, header, playlist_name):
    """
        Params:
            user_id -- id of the given user in config.py
            header -- header of access token
                example -> '{Authorization: Bearer NgCXRK...MzYjw}'
            playlist_name -- name of the list to be created

        If the playlist is successfully created, returns id of created playlist
    """
    url = 'https://api.spotify.com/v1/users/' + user_id + '/playlists'
    data = {'name': playlist_name}
    req = requests.post(url, headers=header, data=json.dumps(data))
    if req.status_code == 201:
        return req.json()['id']
    else:
        return None
