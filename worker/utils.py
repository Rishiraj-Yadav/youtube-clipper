import shutil
import os

def cleanup_job_dir(job_dir: str):
    if os.path.exists(job_dir):
        shutil.rmtree(job_dir)
