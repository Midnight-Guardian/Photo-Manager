"""S3 Client."""
from django.conf import settings
import boto3


class S3BucketClient:
    """Client for s3 bucket."""

    def __init__(self, access_key: str, secret_key: str) -> None:
        """Init params.

        :param access_key: Access key for s3 client
        :param secret_key: Secret access key for s3 client
        """
        self.client_s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    def upload_file_to_s3(self, bucket_name: str, filepath: str, s3_key: str) -> str:
        """Upload file to s3.

        :param bucket_name: PhotoManager bucket name
        :param filepath: local file path
        :param s3_key: Object Key in S3 bucket
        """
        self.client_s3.upload_file(filepath, bucket_name, f'{settings.ENVIRONMENT}/{s3_key}')
        return f'https://{bucket_name}.s3.amazonaws.com/{s3_key}'

    def delete_file_from_s3(self, bucket_name: str, s3_key: str) -> bool:
        """Delete file from s3.

        :param bucket_name: PhotoManager bucket name
        :param s3_key: Object Key in S3 bucket
        """
        self.client_s3.delete_object(Bucket=bucket_name, Key=s3_key)
        return True


def get_s3_bucket_client():
    """Get S3 Bucket Client."""
    return S3BucketClient(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
