# -*- coding: utf-8 -*-

import os
import requests
import base64
import json
import time


class SpotifyAPI:
    def __init__(self, client_id, client_secret, user_name, refresh_token):
        """
            Params:
                client_id (str): client id of your API which register to Spotify.
                client_secret (str): client secret id of your API which register to Spotify.
                user_name (str): name of user
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_name = user_name

        self.refresh_token = refresh_token
        self.access_token = None
        self.api_base_url = 'https://api.spotify.com/v1'


    def __header_base64(self):
        """
            Base 64 encoded string that contains the client ID and client secret key.
        """
        header_base64 = base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode('ascii'))
        header_base64 = str(header_base64).split("'")[1]
        return {'Authorization': f'Basic {header_base64}'}


    def __header_bearer(self):
        return {'Authorization': f'Bearer {self.access_token}'}


    def is_token_expired(self):
        endpoint = '/me'
        url = f'{self.api_base_url}{endpoint}'

        req = requests.get(url, headers=self.__header_bearer())
        return True if req.status_code != 200 else False


    def refresh_access_token(self):
        url = 'https://accounts.spotify.com/api/token'

        body_params = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        req = requests.post(url, data=body_params, headers=self.__header_base64())
        if req.status_code == 200:
            self.access_token = req.json()['access_token']
            return True
        return False


    def search_track(self, keyword):
        """
            Search and get first result of the search.

            Params:
                keyword (str): search keyword
                    example: 'Rammstein Mein Teil'

            Return:
                If track is found return the uri. else False
                    example: spotify:track:39RKlCfLoqb8o2aXfpVfjW
        """
        endpoint = '/search?'
        url = f'{self.api_base_url}{endpoint}'

        params = (
            ('q', keyword),
            ('type', 'track'),
        )

        req = requests.get(url, headers=self.__header_bearer(), params=params)
        if req.status_code == 200:
            items = req.json()['tracks']['items']
            return items[0]['uri'] if items else False
        return False


    def add_track_to_playlist(self, track_uri, playlist_id):
        """
            Add track to given playlist id.

            Params:
                track_uri (str): uri of track.
                    example: 'spotify:track:0h0smRHEjrkSFUhNWQh8SR'
                playlist_id (str): id of the playlist to which the song will be added.

            Return:
                If the song is successfully added, return True. else False
        """
        endpoint = f'/playlists/{playlist_id}/tracks?uris={track_uri}'
        url = f'{self.api_base_url}{endpoint}'

        req = requests.post(url, headers=self.__header_bearer())

        return True if req.status_code == 201 else False


    def list_playlists(self):
        """
            List playlist(s) of the user.

            Return:
                If user has playlist(s), return name and id as list. else False
                    example: [['// G*D', '73hUC4Cy5yTJzirc92YkLM'], [...]]
        """
        endpoint = '/me/playlists'
        url = f'{self.api_base_url}{endpoint}'

        req = requests.get(url, headers=self.__header_bearer())
        if req.status_code == 200:
            items = req.json()
            if 'items' in items:
                return [[item['name'], item['id']] for item in items['items']]
        return False


    def is_playlist_exist(self, playlist_name):
        all_playlists = self.list_playlists()
        if not all_playlists:
            return False

        playlist = [playlist[1] for playlist in all_playlists if playlist[0] == playlist_name]

        return playlist[0] if len(playlist) else False


    def create_playlist(self, playlist_name):
        """
            Create new playlist.

            Params:
                playlist_name (str): name of the playlist

            Return:
                If the playlist is successfully created, return id of playlist. else False
        """
        endpoint = f'/users/{self.user_name}/playlists'
        url = f'{self.api_base_url}{endpoint}'

        data = {
            "name": playlist_name
        }

        req = requests.post(url, headers=self.__header_bearer(), data=json.dumps(data))

        return req.json()['id'] if req.status_code == 201 else False


    def is_track_exist_in_playlist(self, track_id, playlist_id):
        tracks_in_playlist = self.get_track_ids_of_playlist(playlist_id)

        """
        if not tracks_in_playlist:
            return False
        """
        return True if track_id in tracks_in_playlist else False


    def get_track_ids_of_playlist(self, playlist_id):
        """
            Get id of tracks in playlist.

            Params:
                playlist_id (str): id of playlist
         """
        def get_playlist_data(url):
            req = requests.get(url, headers=self.__header_bearer())
            return req.json() if req.status_code == 200 else False

        track_uris = []

        endpoint = f'/playlists/{playlist_id}/tracks'
        url = f'{self.api_base_url}{endpoint}'

        playlist_data = get_playlist_data(url)
        while True:
            if not playlist_data:
                break

            for track in playlist_data['items']:
                track_uris.append(track['track']['uri'])

            if not playlist_data['next']:
                break
            else:
                time.sleep(0.5)
                playlist_data = get_playlist_data(playlist_data['next'])
        return track_uris
