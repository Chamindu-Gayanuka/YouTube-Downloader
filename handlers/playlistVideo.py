import yt_dlp as youtube_dl

def download_playlist(url, quality='best'):
    ydl_opts = {
        'format': quality,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': False,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
        return [entry['title'] for entry in result['entries']]