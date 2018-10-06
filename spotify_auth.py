#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: Batuhan Gürses

import base64
import requests
import urllib.parse
import webbrowser
import json
import config

def authorization_header_base64(client_id, client_secret):
    """
        Makes authorization header.
        Base 64 encoded string that contains the client ID and client secret key.

        Params:
            client_id -- client id of your API which register to Spotify.
            client_secret -- client secret id of your API which register to Spotify.
    """
    auth_header = base64.b64encode((client_id + ':' + client_secret).encode('ascii'))
    auth_header = str(auth_header).split("'")[1]
    return {'Authorization': 'Basic {}'.format(auth_header)}


def request_authorization(client_id, redirect_uri, scope):
    """
        Sends a authorization request to the Spotify Accounts service.

        Params:
            client_id -- client id of your API which register to Spotify.
            redirect_uri -- 'redirect uri' which you have been entered when you register your API.
            scope -- a space-separated list of scopes.
    """
    url = 'https://accounts.spotify.com/authorize/?'
    query_params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope
        }
    url = url + urllib.parse.urlencode(query_params)
    req = requests.get(url)
    webbrowser.open(req.url)


def get_token(auth_code, redirect_uri, auth_header):
    """
        Request refresh and access token.

        Params:
            auth_code -- authorization code.
            redirect_uri -- 'redirect uri' which you have been entered when you register your API.
            auth_header -- base 64 encoded string that contains the client ID and client secret key.

        Returns the refresh and access token.
            example -> [access_token, refresh_token]
    """
    url = 'https://accounts.spotify.com/api/token'
    body_params = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri
        }
    req = requests.post(url, data=body_params, headers=auth_header)
    if req.status_code == 200:
        access_token = req.json()['access_token']
        refresh_token = req.json()['refresh_token']
        return [access_token, refresh_token]
    else:
        return None


def refresh_access_token(refresh_token, auth_header):
    """
        Requesting a refreshed access token.

        Params:
            refresh_token --  the refresh token returned from the authorization code exchange.
            auth_header -- base 64 encoded string that contains the client ID and client secret key.

        Returns a new access token.
    """
    url = 'https://accounts.spotify.com/api/token'
    body_params = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        }
    req = requests.post(url, data=body_params, headers=auth_header)
    if req.status_code == 200:
        return req.json()['access_token']
    else:
        return None
