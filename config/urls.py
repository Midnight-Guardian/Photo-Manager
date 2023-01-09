"""Root URL's config."""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Photo Manager API',
        default_version='v1',
        description="Photo Manager",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

#  Main Url Patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/photo_manager/', include('photo_manager.urls')),
    path('api/user/', include('user.urls'))
]

#  Swagger, ReDoc
urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

#  Token
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_obtain_pair')
]
