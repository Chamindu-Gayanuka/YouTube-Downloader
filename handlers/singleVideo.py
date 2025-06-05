import yt_dlp
from io import BytesIO

def download_video(url: str, quality: str) -> BytesIO:
    ydl_opts = {
        "format": f"bestvideo[height<={quality}]+bestaudio/best",
        "quiet": True,
        "noplaylist": True,
        "prefer_ffmpeg": True,
        "merge_output_format": "mp4",
    }

    buffer = BytesIO()
    buffer.name = "video.mp4"

    def hook(d):
        if d['status'] == 'finished' and 'filename' in d:
            buffer.name = d['filename']

    ydl_opts['progress_hooks'] = [hook]
    ydl_opts['outtmpl'] = "-"  # Avoid writing to disk

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)
        title = result.get("title", "video")
        ext = "mp4"
        buffer.name = f"{title}.{ext}"

        ydl.download([url])
        with open(buffer.name, "rb") as f:
            buffer.write(f.read())
        buffer.seek(0)

    return buffer