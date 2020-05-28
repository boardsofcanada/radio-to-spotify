import requests
import json
import queue
import xml.etree.ElementTree as ET



class RadioStations:
    def __init__(self):
        self.tracks = queue.Queue()


    def __request(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
            }

            req = requests.get(url, headers=headers)

            return req if req.status_code == 200 else False
        except Exception as e:
            print(e)
            return False


    def dark_edge_radio(self):
        req = self.__request("http://darkedge.ro/meta.php")

        if req:
            data = req.json()

            self.tracks.put(data['name'])

            return True
        else:
            return False


    def somafm(self):
        req = self.__request("https://somafm.com/songs/groovesalad.xml")

        if req:
            root = ET.fromstring(req.content.decode())

            song_elem = root.find('song')
            song_name = song_elem.find('title').text
            artist_name = song_elem.find('artist').text

            self.tracks.put(f'{song_name} {artist_name}')

            return True
        else:
            return False


    def main(self):
        self.somafm()
        self.dark_edge_radio()
