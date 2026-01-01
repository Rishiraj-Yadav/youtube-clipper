from fastapi import APIRouter,HTTPException
from app.api.v1.schemas import ClipRequest
from app.services.job_service import create_clip_job
from bson import ObjectId
from app.db.mongodb import db

router = APIRouter()

@router.post("/clip")
async def create_clip(request : ClipRequest):
    job_id = await create_clip_job(request.model_dump())
    
    return {
        "job_id" : job_id,
        "status" : "Pending"
    }
    
@router.get("/clip/{job_id}")
async def get_clip_status(job_id: str):
    job = await db.clip_jobs.find_one({"_id": ObjectId(job_id)})

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job_id,
        "status": job["status"],
        "progress": job.get("progress", 0),
        "status_message": job.get("status_message"),
        "download_url": job.get("download_url"),
        "error_message": job.get("status_message") if job["status"] == "FAILED" else None
    }
