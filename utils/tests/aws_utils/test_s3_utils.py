"""Test Cases for S3 Utils."""
from unittest.mock import patch

from django.test import TestCase
from django.conf import settings
from photo_manager.tests.mocks import boto3_client_mock
from utils.aws_utils.s3_utils import S3BucketClient


class TestS3BucketClient(TestCase):
    """Test Cases for s3 bucket client."""

    @patch('boto3.client', boto3_client_mock)
    def setUp(self) -> None:
        """Set up fixture."""
        self.s3_client = S3BucketClient(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        self.s3_key = 's3_key'
        self.filepath = 'filepath'

    def test_upload_file_to_s3(self):
        """Test upload file to s3.

        We have bucket_name, s3 key name and filepath
        We expect link to the file on the s3
        """
        s3_link = self.s3_client.upload_file_to_s3(bucket_name=settings.AWS_PHOTO_BUCKET_NAME,
                                                   filepath=self.filepath, s3_key=self.s3_key)
        self.assertEqual(s3_link, 'https://test_bucket.s3.amazonaws.com/test/s3_key')
