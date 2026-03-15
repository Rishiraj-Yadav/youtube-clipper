import os
import yt_dlp

COOKIES_PATH = "/etc/secrets/youtube_cookies.txt"


def _build_base_opts() -> dict:
    """Return yt-dlp options, including cookies only if the file exists."""
    opts = {}
    if os.path.isfile(COOKIES_PATH):
        opts["cookies"] = COOKIES_PATH
    return opts


def fetch_video_metadata(youtube_url: str) -> dict:
    ydl_opts = {
        **_build_base_opts(),
        "quiet": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)

    return {
        "duration": info.get("duration"),
        "title": info.get("title")
    }


def download_video(youtube_url: str, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "input.mp4")

    ydl_opts = {
        **_build_base_opts(),
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "outtmpl": output_path,
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    return output_path

