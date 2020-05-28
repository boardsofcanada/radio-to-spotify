# radio-eksen-spotify

[Example playlist](https://open.spotify.com/playlist/05ywtjzHKKQtXaIcMmZs8X?si=EUPQRf_DQbS5Cn_BRdXy_Q)

The app sends a request to each Radio Station for retrieve last played tracks in every each 3 minute. Then, searches the tracks and if tracks is available on Spotify, adds to playlist. Playlists create automatically every day.

Currently working on Dark Edge Radio and SomaFM. More stations can be add. Structure of RadioStation class is suit for this.

# Usage

* Create an app at https://developer.spotify.com/dashboard/applications, enter "http://localhost/" for the **Redirect URIs**


* Change the following lines in **config.py** according to your created spotify app

  ```
  SPOTIFY_USER = 'your spotify user name'
  SPOTIFY_CLIENT_ID = 'client id of your app (from developer.spotify.com)'
  SPOTIFY_CLIENT_SECRET = 'client secret of your app (from developer.spotify.com)'
  SPOTIFY_REDIRECT_URI= 'http://localhost'
  ```
* Run  ```main.py ```

* The script will ask a url for authorize when first run. You just need to copy url from opened web browser and paste it to script.*(After allow your developer account on opened browser.)* **Example** url of you need to paste --> http://localhost/?code=...,

* After paste url, the script creates **refresh_token.txt** and writes refresh token code. The script needs this file to run the program.

# Requirements (tested versions)

  ```
Python >= 3.6
Requests >= 2.20.0
  ```
