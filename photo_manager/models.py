"""Photo Manager Models."""
from django.conf import settings
from rest_framework.authtoken.admin import User
from django.db import models


class Photo(models.Model):
    """The class describing the Photo."""

    s3_image = models.URLField(verbose_name='S3 image URL.')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Created by.', related_name='photos')
    created_at = models.DateField(auto_now_add=True, verbose_name='Created date.')
    geolocation = models.CharField(max_length=256, verbose_name='Photo geolocation', null=True, blank=True)
    description = models.TextField(verbose_name='Photo description.', null=True, blank=True)
    mentions = models.ManyToManyField(User, max_length=512, verbose_name='Mentioned people in the photo..')

    class Meta:
        """Meta Definition."""

        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    @property
    def s3_key(self):
        """Get s3_key."""
        return self.s3_image.split(f'https://{settings.AWS_PHOTO_BUCKET_NAME}.s3.amazonaws.com/')[1]
