from fastapi import FastAPI
from app.api.v1.clip import router as clip_router



app = FastAPI(title = "Youtube Clipper")


app.include_router(clip_router, prefix="/api/v1")




@app.get("/")
def health_check():
    return {
        "status_code":200, "detail":"API is working"
    }