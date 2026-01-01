from app.db.mongodb import db
from app.models.clip_job import ClipJob
from app.queue.redis import redis_client, QUEUE_NAME  

async def create_clip_job(data: dict) -> str:
    job = ClipJob(
        youtube_url=str(data["youtube_url"]),
        start_time=data["start_time"],
        end_time=data["end_time"],
        status="PENDING"
    )

    doc = job.model_dump(
        by_alias=True,
        exclude={"_id"},
        exclude_none=True
    )

    doc["progress"] = 0
    doc["status_message"] = "Waiting for worker"

    result = await db.clip_jobs.insert_one(doc)

    job_id = str(result.inserted_id)

    redis_client.lpush(QUEUE_NAME, job_id)

    return job_id
