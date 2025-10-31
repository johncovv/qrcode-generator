import boto3
import mimetypes

from core import settings


class S3Storage:

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )

    # Uploads a file to S3 and returns its URL
    def upload_file(self, file_path, s3_key) -> str:
        content_type, _ = mimetypes.guess_type(file_path)
        self.s3_client.upload_file(
            file_path,
            self.bucket_name,
            s3_key,
            ExtraArgs={"ContentType": content_type or "application/octet-stream"},
        )
        return self.get_file_url(s3_key)

    # Retrieves a presigned URL for the uploaded file
    def get_file_url(self, s3_key) -> str:
        file_url = self.s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": s3_key,
                "ResponseContentDisposition": "inline",
            },
            ExpiresIn=3600,
        )
        return file_url


storage = S3Storage(bucket_name=settings.aws_s3_bucket_name)
