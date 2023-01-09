"""User API urls."""
from django.urls import path

from user.api import get_partial_matched_names

urlpatterns = [
    path('matched_names/', get_partial_matched_names)
]
