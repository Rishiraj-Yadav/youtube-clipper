import os
from datetime import datetime,timezone
from bson import ObjectId

from worker.db import db
from worker.downloader import fetch_video_metadata, download_video
from worker.clipper import clip_video
from worker.uploader import upload_clip, generate_signed_url
from worker.utils import cleanup_job_dir

TEMP_ROOT = "temp"

MAX_CLIP_SIZE_MB = 10
MAX_CLIP_SIZE_BYTES = MAX_CLIP_SIZE_MB * 1024 * 1024


async def update_progress(job_id: str, progress: int, message: str = None):
    update = {"progress": progress}
    if message:
        update["status_message"] = message

    await db.clip_jobs.update_one(
        {"_id": ObjectId(job_id)},
        {"$set": update}
    )


async def process_job(job_id: str):
    job_dir = None

    try:
        job = await db.clip_jobs.find_one({"_id": ObjectId(job_id)})
        if not job:
            return

        await db.clip_jobs.update_one(
            {"_id": ObjectId(job_id)},
            {
                "$set": {
                    "status": "PROCESSING",
                    "progress": 0,
                    "status_message": "Job started",
                    "started_at": datetime.utcnow()
                }
            }
        )

        # Metadata
        await update_progress(job_id, 10, "Fetching video metadata")
        metadata = fetch_video_metadata(job["youtube_url"])

        if not metadata.get("duration"):
            raise ValueError("Unable to fetch video metadata")

        # Temp dir
        job_dir = os.path.join(TEMP_ROOT, job_id)
        os.makedirs(job_dir, exist_ok=True)

        # Download
        await update_progress(job_id, 30, "Downloading video")
        input_video_path = download_video(
            youtube_url=job["youtube_url"],
            output_dir=job_dir
        )

        # Clip
        await update_progress(job_id, 60, "Clipping video")
        output_video_path = os.path.join(job_dir, "output.mp4")

        clip_mode = clip_video(
            input_path=input_video_path,
            output_path=output_video_path,
            start_time=job["start_time"],
            end_time=job["end_time"]
        )

        # Size check
        await update_progress(job_id, 80, "Checking file size")
        clip_size = os.path.getsize(output_video_path)

        if clip_size > MAX_CLIP_SIZE_BYTES:
            raise ValueError(
                f"Storage limit exceeded: {clip_size / (1024 * 1024):.2f} MB > 20 MB"
            )

        # Upload
        await update_progress(job_id, 90, "Uploading clip")
        storage_key = upload_clip(output_video_path, job_id)
        download_url = generate_signed_url(storage_key)

        # Complete
        await db.clip_jobs.update_one(
            {"_id": ObjectId(job_id)},
            {
                "$set": {
                    "status": "COMPLETED",
                    "progress": 100,
                    "status_message": "Clip ready",
                    "storage_key": storage_key,
                    "download_url": download_url,
                    "file_size_bytes": clip_size,
                    "completed_at": datetime.now(timezone.utc)
                }
            }
        )

    except Exception as e:
        await db.clip_jobs.update_one(
            {"_id": ObjectId(job_id)},
            {
                "$set": {
                    "status": "FAILED",
                    "status_message": str(e),
                    "failed_at": datetime.utcnow()
                }
            }
        )

    finally:
        if job_dir:
            cleanup_job_dir(job_dir)
