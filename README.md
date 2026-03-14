YouTube Clipper

YouTube clipping service built with FastAPI + Redis worker + Streamlit UI.

Storage is configured for DigitalOcean Spaces (S3-compatible), with backward compatibility for existing AWS-style environment variable names.

Features
- Clip any public YouTube video using start and end timestamps.
- Async queue processing using Redis.
- Signed URL download links for generated clips.
- Status tracking for each clip job.
- Separate backend, worker, and frontend services.

Local Development
1. Install dependencies.
	pip install -r requirements.txt
2. Create environment file.
	copy .env.example .env
3. Fill all values in .env (MongoDB, Redis, Spaces, API URLs).
4. Start Redis (local only).
	docker run -d -p 6379:6379 redis:7
5. Start backend.
	uvicorn backend.app.main:app --port 8000
6. Start worker.
	uvicorn worker.web:app --port 8001
7. Start frontend.
	streamlit run frontend/app.py

DigitalOcean Spaces Variables

Preferred variable names:
- SPACES_BUCKET
- SPACES_ACCESS_KEY
- SPACES_SECRET_KEY
- SPACES_REGION
- SPACES_ENDPOINT

Legacy AWS names still supported:
- AWS_S3_BUCKET
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- AWS_S3_ENDPOINT

Production Deployment On DigitalOcean (App Platform)

Prerequisites
1. A DigitalOcean Spaces bucket.
2. Spaces access key and secret.
3. MongoDB URI (Atlas or managed instance).
4. Redis URL (DigitalOcean Managed Redis recommended).
5. GitHub repo connected to DigitalOcean.

Deploy Steps
1. In DigitalOcean, go to App Platform and create app from GitHub repo.
2. Create 3 services using Dockerfiles:
	- backend/Dockerfile
	- worker/Dockerfile
	- frontend/Dockerfile
3. Set run commands if needed:
	- backend: uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
	- worker: uvicorn worker.web:app --host 0.0.0.0 --port 8001
	- frontend: streamlit run frontend/app.py --server.address 0.0.0.0 --server.port 8501
4. Add environment variables to backend and worker:
	- APP_ENV=production
	- MONGODB_URI
	- REDIS_URL
	- SPACES_BUCKET
	- SPACES_ACCESS_KEY
	- SPACES_SECRET_KEY
	- SPACES_REGION (example: sgp1)
	- SPACES_ENDPOINT (example: https://sgp1.digitaloceanspaces.com)
	- SIGNED_URL_TTL_SECONDS=3600
5. Add frontend environment variable:
	- API_BASE_URL=https://<backend-domain>/api/v1
6. Set health check path to / for all services.
7. Deploy and verify:
	- Backend health: GET /
	- Worker health: GET /
	- Frontend loads and can create jobs

Optional App Spec
- A starter DigitalOcean app spec exists at .do/app.yaml.
- Update placeholder values before using it.

Production Notes
- Use managed Redis, not a self-hosted single instance.
- Restrict ALLOWED_ORIGINS to your frontend domain(s).
- Rotate Spaces access keys periodically.
- Keep SIGNED_URL_TTL_SECONDS short (for example 900-3600).
- Monitor worker logs and queue depth.

Single Dockerfile Deployment (All-In-One)

You can also run frontend + backend + worker in one container using the root Dockerfile.

Build
- docker build -t youtube-clipper-all-in-one .

Run
- docker run --env-file .env -p 8501:8501 -p 8000:8000 -p 8001:8001 youtube-clipper-all-in-one

What it starts
- Streamlit frontend on port 8501
- FastAPI backend on port 8000
- Worker web process on port 8001

Notes
- This mode is convenient for simple deployment and demos.
- For production scale/reliability, separate services are still recommended.
