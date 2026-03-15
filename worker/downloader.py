import os
import yt_dlp

COOKIES_PATH = "/etc/secrets/youtube_cookies.txt"

# Player clients tried one-by-one. ios/tv_embedded bypass bot-detection on
# datacenter IPs (Render). We fall through to the next on failure.
_PLAYER_CLIENTS = ["ios", "tv_embedded", "android", "mweb", "web"]

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def _cookies_available() -> bool:
    """Check cookies file and print diagnostic info for Render logs."""
    if os.path.isfile(COOKIES_PATH):
        size = os.path.getsize(COOKIES_PATH)
        print(f"[downloader] Cookies found: {COOKIES_PATH} ({size} bytes)")
        return True
    print(f"[downloader] No cookies at {COOKIES_PATH} — bot detection likely")
    return False


def _build_opts(player_client: str, have_cookies: bool) -> dict:
    """Return yt-dlp options for one player client attempt."""
    opts = {
        "extractor_args": {
            "youtube": {
                "player_client": [player_client],
            }
        },
        "http_headers": {
            "User-Agent": _USER_AGENT,
        },
        "quiet": True,
        "no_warnings": True,
    }
    if have_cookies:
        opts["cookies"] = COOKIES_PATH
    return opts


def _try_each_client(youtube_url: str, extra_opts: dict) -> dict:
    """
    Try every player client in sequence.
    Returns the yt-dlp info dict from the first successful attempt.
    Raises RuntimeError if all clients fail.
    """
    have_cookies = _cookies_available()
    skip = extra_opts.get("skip_download", False)
    last_error = None

    for client in _PLAYER_CLIENTS:
        opts = {**_build_opts(client, have_cookies), **extra_opts}
        try:
            print(f"[downloader] Trying player_client={client}")
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(youtube_url, download=not skip)
            print(f"[downloader] Success with player_client={client}")
            return info
        except Exception as exc:
            print(f"[downloader] player_client={client} failed: {str(exc)[:200]}")
            last_error = exc

    cookies_hint = (
        "Cookies loaded: yes"
        if have_cookies
        else "Cookies NOT loaded — add youtube_cookies.txt as a Render Secret File"
    )
    raise RuntimeError(
        f"All {len(_PLAYER_CLIENTS)} player clients failed. "
        f"{cookies_hint}. Last error: {last_error}"
    )


def fetch_video_metadata(youtube_url: str) -> dict:
    info = _try_each_client(youtube_url, {"skip_download": True})
    return {
        "duration": info.get("duration"),
        "title": info.get("title"),
    }


def download_video(youtube_url: str, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "input.mp4")

    _try_each_client(youtube_url, {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
        "outtmpl": output_path,
        "merge_output_format": "mp4",
    })

    return output_path
