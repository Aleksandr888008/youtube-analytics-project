# This Python file uses the following encoding: utf-8
import requests
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class Video:

    def __init__(self, video_id):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        self.video_title = None
        self.video_url = None
        self.view_count = None
        self.like_count = None

    def get_service_video(self):
        """Заполняет атрибуты экземпляра данными из YouTube API."""
        try:
            checker_url = "https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v="
            video_url = checker_url + self.video_id

            request = requests.get(video_url)

            if request.status_code != 200:
                raise Exception("Такого видео нет")
        except Exception:
            raise Exception

        else:
            response = youtube.videos().list(part='snippet, statistics',
                                             id=self.video_id).execute()

            # Заполняем атрибуты экземпляра данными о канале
            self.video_title = response['items'][0]['snippet']['title']
            self.video_url = f"https://www.youtube.com/video/{self.video_id}"
            self.view_count = response['items'][0]['statistics']['viewCount']
            self.like_count = response['items'][0]['statistics']['likeCount']

    def __str__(self):
        """Возвращает строку с названием видео."""
        response = youtube.videos().list(part='snippet, statistics',
                                         id=self.video_id).execute()
        video_title = response['items'][0]['snippet']['title']
        return f'{video_title}'


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        super().__init__(video_id)
        self.video_id = video_id
        self.video_title = ""
        self.video_url = ""
        self.view_count = 0
        self.like_count = 0
        self.playlist_id = playlist_id
