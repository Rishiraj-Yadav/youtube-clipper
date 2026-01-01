from pydantic import BaseModel, HttpUrl, field_validator

class ClipRequest(BaseModel):
    youtube_url : HttpUrl
    start_time : float
    end_time : float
    
    @field_validator("end_time")
    @classmethod
    
    def validate_time_range(cls,end_time,values):
        
        start_time = values.data.get("start_time")
        
        if start_time is not None and end_time <= start_time:
            raise ValueError("end time must be greater then the start time")
        
        return end_time
    