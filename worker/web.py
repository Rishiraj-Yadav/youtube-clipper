from fastapi import FastAPI
import asyncio
from worker.queue import listen_for_jobs

app = FastAPI()

@app.on_event("startup")
async def start_worker():
    print("🚀 Worker web service started")
    asyncio.create_task(listen_for_jobs())

@app.get("/")
def health():
    return {"status": "worker running"}



# from fastapi import FastAPI
# import threading

# from worker.main import start_worker

# app = FastAPI()

# @app.get("/")
# def health():
#     return {"status": "worker running"}

# threading.Thread(target=start_worker, daemon=True).start()
