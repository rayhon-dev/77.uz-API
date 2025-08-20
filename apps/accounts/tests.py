from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.models import Category

from apps.accounts.models import Address, CustomUser


class AccountsAPITestCase(APITestCase):
    def setUp(self):
        # Test category yaratamiz
        self.category = Category.objects.create(name="Test Category")
        # Test user ma'lumotlari
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
        self.assertIn("id", response.data)
        self.assertEqual(response.data["full_name"], self.user_data["full_name"])
        self.assertEqual(response.data["address"], self.user_data["address"]["name"])

    def test_login_obtain_token(self):
        # Avval user ro'yxatdan o'tadi
        self.test_seller_registration()
        url = reverse("accounts:token_obtain_pair")
        data = {
            "phone_number": self.user_data["phone_number"],
            "password": "testpassword",  # agar CustomUser create method password kerak bo'lsa
        }
        # Agar siz manual password yaratmagan bo'lsangiz, user creationda password qo'shing
        user = CustomUser.objects.get(phone_number=self.user_data["phone_number"])
        user.set_password("testpassword")
        user.is_active = True
        user.save()

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.access_token = response.data["access_token"]  # boshqa testlar uchun saqlaymiz

    def test_token_refresh(self):
        self.test_login_obtain_token()
        url = reverse("accounts:token_refresh")
        data = {"refresh": self.access_token}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_token_verify(self):
        self.test_login_obtain_token()
        url = reverse("accounts:token_verify")
        data = {"token": self.access_token}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("valid", response.data)
        self.assertTrue(response.data["valid"])

    def test_me_endpoint_requires_authentication(self):
        url = reverse("accounts:account-me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Avval login qilamiz
        self.test_login_obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["full_name"], self.user_data["full_name"])

    def test_edit_put_and_patch(self):
        self.test_login_obtain_token()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        url = reverse("accounts:account-edit")

        # PUT (full update)
        put_data = {
            "full_name": "Updated Name",
            "phone_number": "998901234568",
            "address": Address.objects.first().id,
        }
        response = self.client.put(url, put_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["full_name"], "Updated Name")

        # PATCH (partial update)
        patch_data = {"full_name": "Patch Name"}
        response = self.client.patch(url, patch_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["full_name"], "Patch Name")
