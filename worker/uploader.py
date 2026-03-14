import boto3
from botocore.client import Config
from worker.config import settings

session = boto3.session.Session()

s3_client = session.client(
    "s3",
    region_name=settings.STORAGE_REGION,
    endpoint_url=settings.STORAGE_ENDPOINT,
    aws_access_key_id=settings.STORAGE_ACCESS_KEY,
    aws_secret_access_key=settings.STORAGE_SECRET_KEY,
    config=Config(signature_version="s3v4")
)


def upload_clip(local_path: str, job_id: str) -> str:
    object_key = f"clips/{job_id}.mp4"

    s3_client.upload_file(
        Filename=local_path,
        Bucket=settings.STORAGE_BUCKET,
        Key=object_key,
        ExtraArgs={
            "ContentType": "video/mp4"
        }
    )

    return object_key



def generate_signed_url(object_key: str, expires_in: int = 3600) -> str:
    url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": settings.STORAGE_BUCKET,
            "Key": object_key
        },
        ExpiresIn=expires_in or settings.SIGNED_URL_TTL_SECONDS
    )

    return url
