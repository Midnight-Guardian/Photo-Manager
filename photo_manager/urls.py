"""Photo Manager URL's."""
from rest_framework import routers

from photo_manager.api import PhotoCRUD

router = routers.DefaultRouter()
router.register('photo', PhotoCRUD, basename='photo')
urlpatterns = router.urls
