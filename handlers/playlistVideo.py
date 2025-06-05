import yt_dlp
import os

def download_playlist_video(url: str, quality: str) -> list:
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": f"bestvideo[height<={quality}]+bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "quiet": True,
        "noplaylist": False,
        "prefer_ffmpeg": True,
        "merge_output_format": "mp4",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([url])

    files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".mp4")]
    return files