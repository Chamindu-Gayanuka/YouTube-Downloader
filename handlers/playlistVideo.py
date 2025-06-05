import yt_dlp as youtube_dl
from tempfile import NamedTemporaryFile

class VideoObj:
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def __str__(self):
        return self.path

def download_playlist_video(url: str):
    ydl_opts = {
        "quiet": True,
        "extract_flat": "in_playlist",
        "noplaylist": False,
        "format": "best",
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

        if "entries" not in info_dict:
            raise Exception("No videos found in playlist.")

        video_files = []

        for entry in info_dict["entries"]:
            if not entry:
                continue

            video_id = entry.get("id")
            title = entry.get("title", "video")

            with youtube_dl.YoutubeDL({
                "format": "best[ext=mp4]/best",
                "outtmpl": "%(title)s.%(ext)s",
                "quiet": True
            }) as video_ydl:
                temp = NamedTemporaryFile(delete=False, suffix=".mp4")
                video_ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
                video_files.append(VideoObj(temp.name, title + ".mp4"))

        return video_files
