from motor.motor_asyncio import AsyncIOMotorClient 
from ..core.config import settings



client = AsyncIOMotorClient(settings.MONGODB_URI)

db = client.youtube_clipper