🎬 YouTube Clipper

A production-ready YouTube video clipping service that allows users to create short clips from YouTube videos by providing a URL and timestamps.

Built with FastAPI, Redis, async workers, yt-dlp, FFmpeg, MongoDB Atlas, and S3-compatible storage, and designed to run on Render free tier.

🚀 Features

✂️ Clip any public YouTube video using start & end timestamps

⚙️ Asynchronous job processing using Redis + worker service

📦 Secure storage using S3-compatible object storage (DigitalOcean Spaces / AWS S3)

🔐 Signed download URLs (temporary & secure)

📊 Job status tracking (PENDING → PROCESSING → COMPLETED / FAILED)

🧠 Bot-protected YouTube downloads using cookies

🌐 Streamlit frontend for easy usage

☁️ Cloud-ready (Render deployment supported)





▶️ Running Locally
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Start Redis (Docker)
docker run -d -p 6379:6379 redis:7

3️⃣ Start Backend
uvicorn backend.app.main:app --port 8000

4️⃣ Start Worker
uvicorn worker.web:app --port 8001

5️⃣ Start Frontend
streamlit run frontend/app.py
