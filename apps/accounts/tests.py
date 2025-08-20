from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Category

from .models import Address, CustomUser


class AccountsAPITestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.user_data = {
            "full_name": "Test Seller",
            "project_name": "Test Project",
            "phone_number": "998901234567",
            "category": self.category.id,
            "address": {"name": "Tashkent", "lat": 41.3, "long": 69.2},
        }

    def test_seller_registration(self):
        url = reverse("accounts:register-seller")
        response = self.client.post(url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data["data"])
        self.assertEqual(response.data["data"]["full_name"], self.user_data["full_name"])
        self.assertEqual(response.data["data"]["address"], self.user_data["address"]["name"])

    def test_login_obtain_token(self):
        self.test_seller_registration()
        user = CustomUser.objects.get(phone_number=self.user_data["phone_number"])
        user.set_password("testpassword")
        user.is_active = True
        user.save()

        url = reverse("accounts:token_obtain_pair")
        data = {"phone_number": self.user_data["phone_number"], "password": "testpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data["data"])
        self.assertIn("refresh_token", response.data["data"])
        self.access_token = response.data["data"]["access_token"]
        self.refresh_token = response.data["data"]["refresh_token"]

    def test_token_refresh(self):
        self.test_login_obtain_token()
        url = reverse("accounts:token_refresh")
        data = {"refresh": self.refresh_token}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_verify(self):
        self.test_login_obtain_token()
        url = reverse("accounts:token_verify")
        data = {"token": self.access_token}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("valid", response.data["data"])
        self.assertTrue(response.data["data"]["valid"])

    def test_me_endpoint_requires_authentication(self):
        url = reverse("accounts:account-me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.test_login_obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["full_name"], self.user_data["full_name"])

    def test_edit_put_and_patch(self):
        self.test_login_obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse("accounts:account-edit")

        # PUT
        address_id = Address.objects.first().id
        put_data = {
            "full_name": "Updated Name",
            "phone_number": "998901234568",
            "address": address_id,
        }
        response = self.client.put(url, put_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["full_name"], "Updated Name")

        # PATCH
        patch_data = {"full_name": "Patch Name"}
        response = self.client.patch(url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["full_name"], "Patch Name")
