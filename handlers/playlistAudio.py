import yt_dlp as youtube_dl
from tempfile import NamedTemporaryFile

class AudioObj:
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def __str__(self):
        return self.path

def download_playlist_audio(url: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": False,
        "extract_flat": "in_playlist",
        "quiet": True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

        if "entries" not in info_dict:
            raise Exception("No audio found in playlist.")

        audio_files = []

        for entry in info_dict["entries"]:
            if not entry:
                continue

            video_url = entry.get("url")
            title = entry.get("title", "audio")

            with youtube_dl.YoutubeDL({
                "format": "bestaudio/best",
                "outtmpl": "%(title)s.%(ext)s",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "quiet": True
            }) as audio_ydl:
                temp = NamedTemporaryFile(delete=False, suffix=".mp3")
                audio_ydl.download([f"https://www.youtube.com/watch?v={entry['id']}"])
                audio_files.append(AudioObj(temp.name, title + ".mp3"))

        return audio_files