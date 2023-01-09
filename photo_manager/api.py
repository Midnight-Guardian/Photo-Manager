"""Photo API Endpoints."""
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from photo_manager.filters import PhotoFilter
from photo_manager.models import Photo
from photo_manager.serializers import (
    PhotoCreateSerializer, PhotoCreateResponseSerializer,
    PhotoListSerializer, PhotoDetailSerializer, PhotoUpdateSerializer
)
from photo_manager.services import create_photo_and_upload_to_s3, update_photo_metadata
from utils.aws_utils.s3_utils import get_s3_bucket_client


class PhotoCRUD(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin
):
    """Photo View.

    Allows us to Get and Create Photos.
    """

    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PhotoFilter

    def get_queryset(self) -> Photo:
        """Get queryset."""
        return Photo.objects.filter(user_id=self.request.user.id).prefetch_related('mentions')

    def get_serializer_class(self):
        """Get serializer class."""
        if self.action == 'list':
            return PhotoListSerializer
        if self.action == 'retrieve':
            return PhotoDetailSerializer
        if self.action == 'create':
            return PhotoCreateSerializer
        if self.action == 'partial_update':
            return PhotoUpdateSerializer

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: PhotoCreateResponseSerializer()})
    def create(self, request, *args, **kwargs):
        """Create photo obj and upload to S3."""
        request_data = request.data
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        photo = create_photo_and_upload_to_s3(user_id=request.user.id, data=request_data)
        response_serializer = PhotoCreateResponseSerializer(photo)
        return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: PhotoCreateResponseSerializer()})
    def update(self, request, *args, **kwargs):
        """Update photo's metadata."""
        request_data = request.data
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        updated_photo = update_photo_metadata(self.get_object(), request_data)
        response_serializer = PhotoCreateResponseSerializer(updated_photo)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Delete object and remove from s3."""
        get_s3_bucket_client().delete_file_from_s3(settings.AWS_PHOTO_BUCKET_NAME, self.get_object().s3_key)
        super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
