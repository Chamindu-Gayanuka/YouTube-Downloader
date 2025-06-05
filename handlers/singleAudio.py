import yt_dlp as youtube_dl
from tempfile import NamedTemporaryFile

class AudioObj:
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def __str__(self):
        return self.path

def download_audio(url: str) -> AudioObj:
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }
        ],
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title", "audio")
        temp = NamedTemporaryFile(delete=False, suffix=".mp3")
        ydl.download([url])
        return AudioObj(temp.name, title + ".mp3")