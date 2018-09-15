# radio-eksen-spotify

[Example playlist](https://open.spotify.com/user/powerslide1/playlist/0sVzeZN8E7HCGxJQ4XX0PE?si=mpH1i9IGT6quOvXpJFBS-A)

I love discover new musics. Radio Eksen plays songs which I like so much and I don't know. Most of the time, I have been listening live but sometimes I can not. And, I found a solution for this problem.

The app sends a request to Radio Eksen for retrieve last played track in every each one minute. Then, search the track and if track is available on Spotify, adds to playlist. Playlists create automatically every day.  

# Usage

* Create an app at https://developer.spotify.com/dashboard/applications, enter "http://localhost/" for the **Redirect URIs**


* Change the following lines in **config.py** according to your created spotify app

  ```
  SPOTIFY_USER = 'your spotify user name'
  SPOTIFY_CLIENT_ID = 'client id of your app (from developer.spotify.com)'
  SPOTIFY_CLIENT_SECRET = 'client secret of your app (from developer.spotify.com)'
  SPOTIFY_REDIRECT_URI= 'http://localhost'
  ```
* The script will ask a url for authorize when first run. You just need to copy url from opened web browser and paste it to script.*(After allow your developer account on opened browser.)* **Example** url of you need to paste --> http://localhost/?code=...,

* After paste url, the script creates **refresh_token.txt** and writes refresh token code. The script needs this file to run the program.

# Requirements (tested versions)

  ```
Python 3.6.5
Requests 2.18.4
Json 2.0.9
  ```
