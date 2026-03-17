import os
import tempfile
import yt_dlp

COOKIES_PATH = "/etc/secrets/youtube_cookies.txt"
TEMP_COOKIES_PATH = os.path.join(tempfile.gettempdir(), "yt_cookies.txt")

# Player clients tried one-by-one. ios/tv_embedded bypass bot-detection on
# datacenter IPs (Render). We fall through to the next on failure.
_PLAYER_CLIENTS = ["ios", "tv_embedded", "android", "mweb", "web"]

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def _get_cookies_path():
    """Return the path to a valid cookies file, or None if not found."""
    # 1. Check if user passed cookies via environment variable (useful on Render/Heroku)
    cookies_env = os.environ.get("YOUTUBE_COOKIES_CONTENT")
    if cookies_env:
        with open(TEMP_COOKIES_PATH, "w", encoding="utf-8") as f:
            f.write(cookies_env)
        return TEMP_COOKIES_PATH

    # 2. Check the default specific Render secret file
    if os.path.isfile(COOKIES_PATH):
        return COOKIES_PATH

    # 3. Check for ANY .txt file in /etc/secrets that looks like a cookie file
    # This helps if the user named the secret file e.g., "youtube.com_cookies.txt.txt"
    if os.path.isdir("/etc/secrets"):
        for fname in os.listdir("/etc/secrets"):
            if fname.endswith(".txt"):
                fpath = os.path.join("/etc/secrets", fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        if "# Netscape HTTP Cookie File" in f.read(100):
                            return fpath
                except Exception:
                    continue

    return None


def _cookies_available() -> str:
    """Check cookies file and return path to it if found, else None."""
    path = _get_cookies_path()
    if path and os.path.isfile(path):
        size = os.path.getsize(path)
        print(f"[downloader] Cookies found: {path} ({size} bytes)")
        return path
    print("[downloader] No cookies found — bot detection likely")
    return None


def _build_opts(player_client: str, cookies_path: str) -> dict:
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
    if cookies_path:
        opts["cookies"] = cookies_path
        
    proxy_url = os.environ.get("YOUTUBE_PROXY")
    if proxy_url:
        opts["proxy"] = proxy_url
        
    return opts


def _try_each_client(youtube_url: str, extra_opts: dict) -> dict:
    """
    Try every player client in sequence.
    Returns the yt-dlp info dict from the first successful attempt.
    Raises RuntimeError if all clients fail.
    """
    cookies_path = _cookies_available()
    skip = extra_opts.get("skip_download", False)
    last_error = None

    for client in _PLAYER_CLIENTS:
        opts = {**_build_opts(client, cookies_path), **extra_opts}
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
        if cookies_path
        else "Cookies NOT loaded — add youtube_cookies.txt as a Render Secret File or set YOUTUBE_COOKIES_CONTENT env var"
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
