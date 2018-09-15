#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: Batuhan Gürses

import requests

def radio_eksen():
    """
        Returns the recently played 5 songs on Radio Eksen.
            example -> ['Song 1, 'Song 2', 'Song 3', 'Song 4', 'Song 5']
    """
    url = 'http://radioeksen.com/Json/GetLast5Song'
    req = requests.get(url)
    tracks = []
    for track in req.json():
        tracks.append(track['Artist'] + ' ' + track['TrackName'])
    return tracks
