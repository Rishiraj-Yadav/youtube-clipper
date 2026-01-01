# from motor.motor_asyncio import AsyncIOMotorClient
# import os

# MONGODB_URI = os.getenv("MONGODB_URI")

# client = AsyncIOMotorClient(MONGODB_URI)
# db = client.youtube_clipper



from motor.motor_asyncio import AsyncIOMotorClient
from worker.config import MONGODB_URI

client = AsyncIOMotorClient(MONGODB_URI)
db = client.youtube_clipper
