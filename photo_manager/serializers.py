"""Serializers for Photo Manager API."""
from rest_framework.authtoken.admin import User
from rest_framework import serializers, status
from django.core.validators import validate_image_file_extension
from rest_framework.exceptions import ValidationError

from photo_manager.models import Photo


class PhotoCreateSerializer(serializers.Serializer):
    """Serializer for PhotoCRUD API."""

    photo = serializers.ImageField(required=True, validators=(validate_image_file_extension,))


class PhotoUpdateSerializer(serializers.ModelSerializer):
    """Serializer for update photo PhotoCRUD API."""

    mentions = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        """Meta Definition."""

        model = Photo
        fields = (
            'geolocation',
            'description',
            'mentions',
        )

    def validate_mentions(self, value: list) -> str:
        """Validator for people in the photo."""
        found_users = set(User.objects.filter(username__in=value).values_list('username', flat=True))

        set_value = set(value)
        if found_users != set_value:
            raise ValidationError(f'Users with names {set_value.difference(found_users)} are not found.',
                                  code=status.HTTP_400_BAD_REQUEST)
        return value


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    class Meta:
        """Meta Definition."""

        model = User
        fields = ('id', 'username')


class PhotoCreateResponseSerializer(serializers.ModelSerializer):
    """Photo Create Serializer."""

    user = UserSerializer(read_only=True)

    class Meta:
        """Meta Definition."""

        model = Photo
        fields = ('id', 'user', 's3_image', 'created_at')


class PhotoDetailSerializer(serializers.ModelSerializer):
    """Photo Detail Serializer."""

    user = UserSerializer(read_only=True, many=False)
    mentions = serializers.ManyRelatedField(child_relation=UserSerializer())

    class Meta:
        """Meta Definition."""

        model = Photo
        fields = '__all__'


class PhotoListSerializer(serializers.ModelSerializer):
    """Photo List Serializer."""

    class Meta:
        """Meta Definition."""

        model = Photo
        fields = ('s3_image',)
