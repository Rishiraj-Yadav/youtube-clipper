import os
from dotenv import load_dotenv, find_dotenv

# Load env as early as possible
load_dotenv(find_dotenv())

MONGODB_URI = os.getenv("MONGODB_URI")
REDIS_URL = os.getenv("REDIS_URL")

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI is not set")

if not REDIS_URL:
    raise RuntimeError("REDIS_URL is not set")
