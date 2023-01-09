"""User API."""
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from photo_manager.serializers import UserSerializer
from user.services import get_matched_users


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'name', openapi.IN_QUERY,
            description="Username. Get up to 5 usernames which are partially matched.",
            type=openapi.TYPE_STRING)],
    operation_description='Get up to 5 usernames.',
    responses={status.HTTP_200_OK: UserSerializer(many=True)})
@api_view(['GET'])
def get_partial_matched_names(request):
    """Return the list of up to 5 names."""
    matched_users = get_matched_users(request.query_params.get('name', ''))
    return Response(data=UserSerializer(matched_users, many=True).data, status=status.HTTP_200_OK)




