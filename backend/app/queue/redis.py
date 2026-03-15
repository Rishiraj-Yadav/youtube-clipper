from redis import asyncio as aioredis
from ..core.config import settings

# Use async Redis so lpush is non-blocking inside async FastAPI handlers (Bug 3 fix)
redis_client = aioredis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
)

QUEUE_NAME = "clip_jobs"
