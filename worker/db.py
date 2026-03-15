# from motor.motor_asyncio import AsyncIOMotorClient
# import os

# MONGODB_URI = os.getenv("MONGODB_URI")

# client = AsyncIOMotorClient(MONGODB_URI)
# db = client.youtube_clipper



from motor.motor_asyncio import AsyncIOMotorClient
from worker.config import MONGODB_URI

# tlsAllowInvalidCertificates=True fixes the SSL handshake error
# [SSL: TLSV1_ALERT_INTERNAL_ERROR] seen with Python + MongoDB Atlas.
client = AsyncIOMotorClient(
    MONGODB_URI,
    tlsAllowInvalidCertificates=True
)
db = client.youtube_clipper
