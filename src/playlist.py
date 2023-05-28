import datetime
import os
import isodate
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:

    def __init__(self, playlist_id: str) -> None:
        """Инициализируем сначала ID и URL плейлиста, затем его название"""
        self.id = playlist_id
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"

        self.playlists_info = youtube.playlists().list(id=self.id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50,
                                                       ).execute()

        self.videos_info = youtube.playlistItems().list(playlistId=self.id,
                                                        part='contentDetails',
                                                        maxResults=50,
                                                        ).execute()

        self.videos_id: list[str] = [video['contentDetails']['videoId'] for video in self.videos_info['items']]

        self.video_response = youtube.videos().list(part='contentDetails, statistics',
                                                    id=','.join(self.videos_id)
                                                    ).execute()

        self.title = self.playlists_info['items'][0]['snippet']['title']

    @property
    def total_duration(self):
        """Выводим общую длительность плейлиста"""
        total_duration = datetime.timedelta()
        video_response = self.video_response

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration1 = isodate.parse_duration(iso_8601_duration)
            total_duration += duration1

        return total_duration

    def show_best_video(self):
        """Вывод видео с наибольшим количеством лайков"""
        most_likes = 0
        count = int(len(self.video_response['items']))
        most_likes_video = None

        for i in range(count):
            like_count = int(self.video_response['items'][i]['statistics']['likeCount'])

            if like_count > most_likes:
                most_likes = like_count
                most_likes_video = self.video_response['items'][i]['id']

        return f"https://youtu.be/{most_likes_video}"

