"""S3-based file storage utilities."""

from __future__ import annotations

import uuid
from typing import BinaryIO, Optional

import boto3
from botocore.client import Config

from app.core.config import settings


def _get_s3_client():
    return boto3.client(
        "s3",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version="s3v4"),
    )


def generate_profile_photo_key(user_id: int, filename: str) -> str:
    """Generate a unique S3 key for a user's profile photo."""
    ext = ""
    if "." in filename:
        ext = filename.rsplit(".", 1)[1].lower()
    unique_id = uuid.uuid4().hex
    return f"profiles/{user_id}/{unique_id}.{ext or 'jpg'}"


def upload_file_obj(
    file_obj: BinaryIO,
    bucket: str,
    key: str,
    content_type: Optional[str] = None,
) -> str:
    """Upload a file-like object to S3 and return its public URL."""
    s3 = _get_s3_client()

    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type

    s3.upload_fileobj(file_obj, bucket, key, ExtraArgs=extra_args)

    return f"https://{bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"


def delete_file(bucket: str, key: str) -> None:
    """Delete an object from S3."""
    s3 = _get_s3_client()
    s3.delete_object(Bucket=bucket, Key=key)
