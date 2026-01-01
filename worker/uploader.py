import boto3
import os
from botocore.client import Config

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_S3_ENDPOINT = os.getenv("AWS_S3_ENDPOINT")

session = boto3.session.Session()

s3_client = session.client(
    "s3",
    region_name=AWS_REGION,
    endpoint_url=AWS_S3_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=Config(signature_version="s3v4")
)


def upload_clip(local_path: str, job_id: str) -> str:
    object_key = f"clips/{job_id}.mp4"

    s3_client.upload_file(
        Filename=local_path,
        Bucket=AWS_S3_BUCKET,
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
            "Bucket": AWS_S3_BUCKET,
            "Key": object_key
        },
        ExpiresIn=expires_in
    )

    return url
