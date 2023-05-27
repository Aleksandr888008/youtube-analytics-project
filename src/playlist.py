# This Python file uses the following encoding: utf-8
import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id):
        """Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API."""
        self.playlist_id = playlist_id
        self.title = ''
        self.url = ''

    def get_service_playlist(self):
        """Заполняет атрибуты экземпляра данными из YouTube API."""

        response = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                part='contentDetails',
                                                maxResults=50,
                                                ).execute()

        # Заполняем атрибуты экземпляра данными о канале
        #self.title = response['items']['snippet']['title']
        #self.url = f"https://www.youtube.com/playlist/{self.playlist_id}"
        #return response


# if __name__ == '__main__':
#     pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
#
#     print(json.dumps(pl.get_service_playlist()))
