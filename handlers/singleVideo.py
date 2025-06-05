import yt_dlp as youtube_dl
from tempfile import NamedTemporaryFile

class VideoObj:
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def __str__(self):
        return self.path

def download_video(url: str) -> VideoObj:
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title", "video")
        temp = NamedTemporaryFile(delete=False, suffix=".mp4")
        ydl.download([url])
        return VideoObj(temp.name, title + ".mp4")