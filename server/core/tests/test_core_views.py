import json

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from core.models import AppUser


class TestCoreViews(APITestCase):
    def setUp(self):
        pass

    def test_sign_up_works_correctly_for_proper_fields(self):
        self.proper_user_fields = {
            "username": "testuser123",
            "password": "testuser123",
        }
        response = self.client.post(reverse('create_user'), self.proper_user_fields)
        u = AppUser.objects.get(username="testuser123")
        token = Token.objects.get(user=u)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content)['auth_token'], token.key)

    def test_sign_up_fails_on_no_username(self):
        no_username_payload = {
            "password": "testuser123"
        }
        count_of_users = AppUser.objects.all().count()
        response = self.client.post(reverse('create_user'), no_username_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(count_of_users, AppUser.objects.all().count())

    def test_sign_up_fails_on_no_password(self):
        no_password_payload = {
            "username": "test123"
        }
        count_of_users = AppUser.objects.all().count()
        response = self.client.post(reverse("create_user"), no_password_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(count_of_users, AppUser.objects.all().count())
