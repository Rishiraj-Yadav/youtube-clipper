from redis import asyncio as aioredis
from ..core.config import settings

# Use async Redis so lpush is non-blocking inside async FastAPI handlers.
# ssl_cert_reqs=None is required for DigitalOcean Managed Redis which uses
# rediss:// (SSL) with a certificate that Python's ssl module rejects by default.
redis_client = aioredis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    ssl_cert_reqs=None,
)

QUEUE_NAME = "clip_jobs"
