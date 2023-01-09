"""Filters for Photo Manager API."""
from django_filters.rest_framework import FilterSet, DateFilter, CharFilter
from photo_manager.models import Photo


class PhotoFilter(FilterSet):
    """Photo API Filter."""

    created_at = DateFilter(field_name='created_at')
    mentions = CharFilter(field_name='mention', lookup_expr='icontains')
    geolocation = CharFilter(field_name='geolocation', lookup_expr='icontains')

    class Meta:
        """Meta definition."""

        model = Photo
        fields = ("created_at",)
