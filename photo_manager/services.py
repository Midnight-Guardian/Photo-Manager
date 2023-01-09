"""Photo Manager Services."""
import uuid

from django.conf import settings
from rest_framework.authtoken.admin import User

from photo_manager.models import Photo
from utils.aws_utils.s3_utils import get_s3_bucket_client


def generate_photo_s3_key(user_id: int, content_type: str) -> str:
    """Generate s3 key for photo."""
    return f"{settings.ENVIRONMENT}/{user_id}/{uuid.uuid4().hex}.{content_type.split('/')[1]}"


def create_photo_and_upload_to_s3(user_id: int, data: dict) -> Photo:
    """Upload user photo to s3.

    :param user_id: ID of the user
    :param data: Image data
    """
    photo = data.pop('photo')[0]
    s3_key = generate_photo_s3_key(user_id, photo.content_type)
    s3_image = get_s3_bucket_client().upload_file_to_s3(
        settings.AWS_PHOTO_BUCKET_NAME,
        photo.temporary_file_path(), s3_key)
    photo = Photo.objects.create(user_id=user_id, s3_image=s3_image, **data)
    return photo


def update_photo_metadata(photo: Photo, data) -> Photo:
    """Update photo metadata and return object."""
    mentions = data.pop('mentions', None)
    Photo.objects.filter(id=photo.id).update(**data)
    if mentions:
        users = User.objects.filter(username__in=mentions)
        photo.mentions.set(users)
    return photo
