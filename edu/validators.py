import re
from rest_framework.serializers import ValidationError

ALLOW_DOMAINS = [
    "youtube.com",
    "youtube.ru",
    "googlevideo.com",
    "ytimg.com",
    "youtu.be",
]


class YoutubeOnly:
    """
    Проверка на отсутствие ссылок кроме youtube.com
    Класс принимает список полей на проверку
    """

    def __init__(self, fields):
        self.fields = fields[:]

    def __call__(self, data):
        for key, value in data.items():
            if key not in self.fields:
                continue

            domains = re.split(r"[hH][tT][tT][pP][sS]?://", value)
            for word in domains[1:]:
                domain = word.split(" ")[0].split("/")[0]
                if domain not in ALLOW_DOMAINS:
                    raise ValidationError(f"[{key}]: Allowed references from YouTube only! Not {domain}")
