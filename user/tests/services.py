"""Services Test Cases."""
from django.test import TestCase
from rest_framework.authtoken.admin import User

from user.services import get_matched_users


class TestCaseServices(TestCase):
    """Test Cases for services."""

    def setUp(self) -> None:
        """Set up fixture."""
        for i in range(7):
            User.objects.create_user(username=f'test{i}', password=f'test{i}')

    def test_get_matched_users(self):
        """Test Get Matched Users with test in param

        We have 7 users. We expect that only 5 users will be returned.
        """
        users = get_matched_users(name='test')
        self.assertEqual(len(users), 5)
        for user in users:
            self.assertIn('test', user['username'])

    def test_get_matched_users_wo_param(self):
        """Test Get Matched User with empty string as param.

        We have 7 users. We expect that only 5 users will be returned.
        """
        users = get_matched_users(name='')
        self.assertEqual(len(users), 5)

    def test_get_matched_one_user(self):
        """

        We have 7 users and only one user has number 5 in his nickname.
        We expect queryset with this one user.
        """
        users = get_matched_users(name='5')
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['username'], 'test5')
