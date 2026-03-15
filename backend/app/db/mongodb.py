from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings


# tlsAllowInvalidCertificates=True fixes the SSL handshake error
# [SSL: TLSV1_ALERT_INTERNAL_ERROR] seen with Python 3.11+ and MongoDB Atlas.
client = AsyncIOMotorClient(
    settings.MONGODB_URI,
    tlsAllowInvalidCertificates=True
)

db = client.youtube_clipper