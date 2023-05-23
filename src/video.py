# This Python file uses the following encoding: utf-8

import os
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class Video:

    def __init__(self, video_id):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        self.video_title = ""
        self.video_url = ""
        self.view_count = 0
        self.like_count = 0

    def get_service_video(self):
        """Заполняет атрибуты экземпляра данными из YouTube API."""

        response = youtube.videos().list(part='snippet, statistics, contentDetails,topicDetails',
                                         id=self.video_id).execute()

        # Заполняем атрибуты экземпляра данными о канале
        self.video_title = response['items'][0]['snippet']['title']
        self.video_url = f"https://www.youtube.com/channel/{self.video_id}"
        self.view_count = response['items'][0]['statistics']['viewCount']
        self.like_count = response['items'][0]['statistics']['likeCount']


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        super().__init__(video_id)
        self.video_title = ""
        self.video_url = ""
        self.view_count = 0
        self.like_count = 0
        self.playlist_id = playlist_id
