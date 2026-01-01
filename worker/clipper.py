import subprocess
import os

def clip_video(
    input_path: str,
    output_path: str,
    start_time: float,
    end_time: float
):
    duration = end_time - start_time

    # Attempt fast stream copy first
    stream_copy_cmd = [
        "ffmpeg",
        "-y",
        "-ss", str(start_time),
        "-i", input_path,
        "-t", str(duration),
        "-c", "copy",
        output_path
    ]

    try:
        subprocess.run(
            stream_copy_cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return "copy"

    except subprocess.CalledProcessError:
        # Fallback to re-encode
        reencode_cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(start_time),
            "-i", input_path,
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "fast",
            "-c:a", "aac",
            output_path
        ]

        subprocess.run(
            reencode_cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return "reencode"
