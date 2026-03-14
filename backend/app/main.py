from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.clip import router as clip_router
from .core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(clip_router, prefix="/api/v1")




@app.get("/")
def health_check():
    return {
        "status_code": 200,
        "detail": "API is working",
        "environment": settings.APP_ENV,
        "version": settings.APP_VERSION,
    }