import json
import os
from googleapiclient.discovery import build

api_key: str = os.getenv('API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = ""
        self.description = ""
        self.url = ""
        self.subscriber_count = 0
        self.video_count = 0
        self.view_count = 0

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel))

    def get_service(self):
        """Заполняет атрибуты экземпляра данными из YouTube API."""

        response = youtube.channels().list(
            part="snippet,statistics",
            id=self.__channel_id
        ).execute()

        # Получаем данные о канале из ответа API
        channel = response['items'][0]
        snippet = channel['snippet']
        statistics = channel['statistics']

        # Заполняем атрибуты экземпляра данными о канале
        self.title = snippet['title']
        self.description = snippet['description']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = int(statistics['subscriberCount'])
        self.video_count = int(statistics['videoCount'])
        self.view_count = int(statistics['viewCount'])

    def to_json(self):
        """Сохраняет значения атрибутов экземпляра Channel в файл в формате json."""
        with open('vdud.json', "w") as f:
            json.dump({
                "id": self.__channel_id,
                "name": self.title,
                "description": self.description,
                "link": self.url,
                "subscribers": self.subscriber_count,
                "video_count": self.video_count,
                "view_count": self.view_count,
            }, f)

    def __str__(self):
        """Возвращает строку с названием и ссылкой на канал."""

        channel = youtube.channels().list(id=self.__channel_id, part='snippet').execute()
        snippet = channel['items'][0]['snippet']
        return f"{snippet['title']} (https://www.youtube.com/channel/{self.__channel_id})"

    def __add__(self, other):
        """Складывает два канала по количеству подписчиков."""

        subs1 = self.get_subscribers_count()
        subs2 = other.get_subscribers_count()
        return subs1 + subs2

    def __sub__(self, other):
        """Вычитает два канала по количеству подписчиков."""

        subs1 = self.get_subscribers_count()
        subs2 = other.get_subscribers_count()
        return subs1 - subs2

    def __lt__(self, other):
        """Сравнивает два канала по количеству подписчиков."""

        subs1 = self.get_subscribers_count()
        subs2 = other.get_subscribers_count()
        return subs1 < subs2

    def __gt__(self, other):
        """Сравнивает два канала по количеству подписчиков."""

        subs1 = self.get_subscribers_count()
        subs2 = other.get_subscribers_count()
        return subs1 > subs2

    def __le__(self, other):
        """Сравнивает два канала по количеству подписчиков."""

        subs1 = self.get_subscribers_count()
        subs2 = other.get_subscribers_count()
        return subs1 <= subs2

    def __ge__(self, other):
        """Сравнивает два канала по количеству подписчиков."""

        subs1 = self.get_subscribers_count()
        subs2 = other.get_subscribers_count()
        return subs1 >= subs2

    def __eq__(self, other):
        """Сравнивает два канала по количеству подписчиков."""

        subs1 = self.get_subscribers_count()
        subs2 = other.get_subscribers_count()
        return subs1 == subs2

    def get_subscribers_count(self) -> int:
        """Возвращает количество подписчиков канала."""

        channel = youtube.channels().list(id=self.__channel_id, part='statistics').execute()
        return int(channel['items'][0]['statistics']['subscriberCount'])
