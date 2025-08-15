import os
import tempfile
import yt_dlp

def download_video(url: str) -> str:
    """
    Downloads a video from a URL and saves it to a temporary directory.

    Args:
        url: The URL of the video to download.

    Returns:
        The file path of the downloaded video.
    """
    temp_dir = tempfile.mkdtemp()
    ydl_opts = {
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)