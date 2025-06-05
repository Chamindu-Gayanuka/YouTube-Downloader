import yt_dlp
from io import BytesIO

def download_audio(url: str, quality: str) -> BytesIO:
    ydl_opts = {
        "format": f"bestaudio[abr<={quality}]",
        "outtmpl": "-",
        "quiet": True,
        "noplaylist": True,
        "prefer_ffmpeg": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": quality,
            }
        ],
    }

    buffer = BytesIO()
    buffer.name = "audio.mp3"

    def hook(d):
        if d['status'] == 'finished' and 'filename' in d:
            buffer.name = d['filename']

    ydl_opts['progress_hooks'] = [hook]
    ydl_opts['outtmpl'] = "-"  # Output to stdout

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)
        title = result.get("title", "audio")
        ext = result.get("ext", "mp3")
        buffer.name = f"{title}.{ext}"

        ydl.download([url])
        with open(buffer.name, "rb") as f:
            buffer.write(f.read())
        buffer.seek(0)

    return buffer