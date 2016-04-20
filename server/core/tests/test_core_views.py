import json

from django.contrib.auth.models import User
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

    def test_api_docs_is_visible_if_user_is_logged_in(self):
        AppUser.objects.create_superuser(username="admin", email="admin@admin.com", password="admin")
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse("drfdocs"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_docs_is_not_visible_for_non_logged_in_users(self):
        response = self.client.get(reverse("drfdocs"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_user_and_request_for_pickup(self):
        a = AppUser.objects.create(username="admin", email="admin@admin.com", password="admin", is_staff=True)
        a.set_password("admin")
        a.save()
        request_payload_with_proper_params = {
            "pickup_latitude": 37.336065,
            "pickup_longitude": -121.886406,
            "drop_off_latitude": 37.336065,
            "drop_off_longitude": -121.886406
        }

        self.client.login(username="admin", password="admin")
        response = self.client.post(reverse("request_ride"), request_payload_with_proper_params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_with_no_pickup_details_latitude_throws_error(self):
        a = AppUser.objects.create(username="admin", email="admin@admin.com", password="admin", is_staff=True)
        a.set_password("admin")
        a.save()
        request_payload_with_improper_params = {
            "pickup_longitude": -121.886406,
            "drop_off_latitude": 37.336065,
            "drop_off_longitude": -121.886406
        }
        self.client.login(username="admin", password="admin")
        response = self.client.post(reverse("request_ride"), request_payload_with_improper_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_with_no_auth_will_return_no_auth_message(self):
        request_payload_with_proper_params = {
            "pickup_latitude": 37.336065,
            "pickup_longitude": -121.886406,
            "drop_off_latitude": 37.336065,
            "drop_off_longitude": -121.886406
        }
        response = self.client.post(reverse("request_ride"), request_payload_with_proper_params)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
