# -*- coding: utf-8 -*-

import base64
import requests
import webbrowser
import os


class SpotifyAuthorization:
    """
        Authorize your application.
        After authorize, 'refresh token' code writes to 'refresh_token.txt' for refreshing 'access token'

        Example use of:
            - a = SpotifyAuthorization(client_id, client_secret, redirect_uri, scope)
            - a.main()
    """
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        """
            Params:
                client_id (str): client id of your API which register to Spotify.
                client_secret (str): client secret id of your API which register to Spotify.
                redirect_uri (str): redirect uri which you have been entered when you register your API.
                scope (str): a space-separated list of scopes.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

        self.refresh_token = None
        self.refresh_token_file = "{0}/{1}".format(os.path.dirname(os.path.abspath(__file__)), "refresh_token.txt")


    def __header_base64(self):
        """
            Base 64 encoded string that contains the client ID and client secret key.
        """
        header_base64 = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode('ascii'))
        header_base64 = str(header_base64).split("'")[1]
        return {'Authorization': f'Basic {header_base64}'}


    def __request_authorization(self):
        """
            Send an authorization request.
        """
        url = 'https://accounts.spotify.com/authorize/?'
        params = (
            ('client_id', self.client_id),
            ('response_type', 'code'),
            ('redirect_uri', self.redirect_uri),
            ('scope', self.scope),
        )

        req = requests.get(url, params=params)
        if req.status_code == 200:
            webbrowser.open(req.url)
            return True
        else:
            return False


    def __request_access_token(self, auth_code):
        """
            Request the access token and get refresh token

            Params:
                auth_code (str): authorization code.
        """
        url = 'https://accounts.spotify.com/api/token'
        body_params = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri
        }

        req = requests.post(url, data=body_params, headers=self.__header_base64())
        if req.status_code == 200:
            self.refresh_token = req.json()['refresh_token']
            return True
        else:
            return False


    def __check_refresh_token(self):
        """
            Check the refresh token file. If found, get refresh token code.
        """
        try:
            if os.stat(self.refresh_token_file).st_size == 0:
                return False
            else:
                with open(self.refresh_token_file, 'r') as filehandler:
                    self.refresh_token = filehandler.readline().strip()
                return True
        except FileNotFoundError:
            return False


    def __write_refresh_token(self):
        with open(self.refresh_token_file, 'a') as file:
            file.truncate(0)
            file.write(self.refresh_token)
        print("Refresh token code written to file")
        return True


    def main(self):
        if self.__check_refresh_token():
            return True
        else:
            if not self.__request_authorization():
                return False

            auth_code = input('Please paste url: (Ex. http://localhost/?code=AQB.....) \n')
            if '#_=_' in auth_code:
                auth_code =  auth_code.split('#')[0]
            auth_code = auth_code.split('?code=')[-1]

            if self.__request_access_token(auth_code):
                self.__write_refresh_token()
                return True
            else:
                return False
