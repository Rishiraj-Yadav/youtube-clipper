import redis
from app.core.config import settings

redis_client = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    # ssl=True,
    # ssl_cert_reqs=None
)

QUEUE_NAME = "clip_jobs"
