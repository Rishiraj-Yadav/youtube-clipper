import os
import yt_dlp

COOKIES_PATH = "/etc/secrets/youtube_cookies.txt"

# yt-dlp player clients to try in order.
# tv_embedded / ios / android bypass YouTube's bot-detection challenge
# which blocks plain web requests from datacenter IPs (e.g. Render).
_PLAYER_CLIENTS = ["tv_embedded", "ios", "android", "web"]

# A realistic browser User-Agent reduces bot-detection probability.
_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def _build_base_opts() -> dict:
    """
    Return base yt-dlp options.
    - Uses cookies file if it exists on Render (Secret File).
    - Uses mobile/TV player clients to bypass bot-detection on server IPs.
    """
    opts = {
        "extractor_args": {
            "youtube": {
                "player_client": _PLAYER_CLIENTS,
            }
        },
        "http_headers": {
            "User-Agent": _USER_AGENT,
        },
    }
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
        # Prefer mp4 video + m4a audio. Falls back to any available mp4.
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best",
        "outtmpl": output_path,
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    return output_path

