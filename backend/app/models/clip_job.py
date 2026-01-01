from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field

class ClipJob(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    youtube_url: str
    start_time: float
    end_time: float
    status: str
    output_url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Config:
        populate_by_name = True
