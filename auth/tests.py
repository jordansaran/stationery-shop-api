from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class AuthTest(APITestCase):

    fixtures = ["users.json"]

    def test_get_user(self):
        user: User = User.objects.get(pk=1)
        self.assertEqual(user.username, "saleadmin")
        self.assertEqual(user.email, "sale@gmail.com")
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_superuser, True)
