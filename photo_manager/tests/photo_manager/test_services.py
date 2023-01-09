"""Tests Cases for Photo Manager Services."""
from unittest.mock import patch

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from rest_framework.authtoken.admin import User

from photo_manager.models import Photo
from photo_manager.services import create_photo_and_upload_to_s3, update_photo_metadata, generate_photo_s3_key
from photo_manager.tests.mocks import boto3_client_mock, uuid4_mock


@patch('utils.aws_utils.s3_utils.boto3.client', boto3_client_mock)
class TestCasesServices(TestCase):
    """Test Cases for Services."""

    def setUp(self) -> None:
        """Set up fixture."""
        self.user = User.objects.create_user(username='test', password='test')
        self.photo = InMemoryUploadedFile(None, 'photo', 'TestPhoto.png', 'image/png', 123, None)
        self.photo.temporary_file_path = lambda: 'filepath'
        self.photo_data = {
            'photo': [self.photo]
        }
        self.photo_metadata = {
            'geolocation': 'test geolocation',
            'mentions': ['test'],
            'description': 'test_description'
        }

    @patch('uuid.uuid4', uuid4_mock)
    def test_create_photo_and_upload_to_s3(self):
        """Test create photo and upload to s3.

        We have user_id and photo data
        """
        photo = create_photo_and_upload_to_s3(user_id=self.user.id, data=self.photo_data)
        self.assertEqual(photo.s3_image, 'https://test_bucket.s3.amazonaws.com/test/1/hex.png')

    def test_update_photo_metadata(self):
        """Test update photo metadata."""
        photo = Photo.objects.create(user_id=self.user.id, s3_image='https://test.com')
        photo = update_photo_metadata(photo, self.photo_metadata.copy())
        photo.refresh_from_db()
        self.assertEqual(photo.geolocation, self.photo_metadata['geolocation'])
        self.assertEqual(photo.description, self.photo_metadata['description'])
        self.assertEqual(list(photo.mentions.values_list('username', flat=True)), self.photo_metadata['mentions'])

    @patch('uuid.uuid4', uuid4_mock)
    def test_generate_photo_s3_key(self):
        """Test Generate Photo s3 key."""
        s3_key = generate_photo_s3_key(user_id=self.user.id, content_type='image/png')
        self.assertEqual(s3_key, 'test/1/hex.png')
