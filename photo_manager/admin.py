"""Photo Manager Admin Config."""
from django.contrib import admin
from .models import Photo


admin.site.register(Photo)
