"""User Services."""
from rest_framework.authtoken.admin import User


def get_matched_users(name: str) -> list[User]:
    """Return up to 5 matched users."""
    return User.objects.filter(username__icontains=name).values('username')[:5]
