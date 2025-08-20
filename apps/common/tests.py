from common.models import District, Page, Region, Setting
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CommonAPITestCase(APITestCase):
    def setUp(self):
        # Regions va Districts
        self.region = Region.objects.create(name="Tashkent Region")
        self.district = District.objects.create(region=self.region, name="Yunusobod")

        # Page
        self.page = Page.objects.create(title="Home", content="Welcome to Home Page")

        # Settings
        self.setting = Setting.objects.create(
            phone="+998901234567",
            support_email="support@test.com",
            working_hours="9:00 - 18:00",
            app_version="1.0.0",
            maintenance_mode=False,
        )

    # ------------------ Page List ------------------
    def test_page_list(self):
        url = reverse("common:pages-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        # Pagination bilan ishlash: data['results'] list bo'ladi
        self.assertIsInstance(response.data["data"]["results"], list)
        self.assertIn("slug", response.data["data"]["results"][0])
        self.assertIn("title", response.data["data"]["results"][0])

    # ------------------ Page Detail ------------------
    def test_page_detail(self):
        url = reverse("common:pages-detail", args=[self.page.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["slug"], self.page.slug)
        self.assertEqual(response.data["data"]["title"], self.page.title)
        self.assertEqual(response.data["data"]["content"], self.page.content)

    # ------------------ Regions with Districts ------------------
    def test_regions_with_districts(self):
        url = reverse("common:regions-with-districts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertIsInstance(response.data["data"], list)
        region_data = response.data["data"][0]
        self.assertEqual(region_data["id"], self.region.id)
        self.assertEqual(region_data["name"], self.region.name)
        self.assertIsInstance(region_data["districts"], list)
        self.assertEqual(region_data["districts"][0]["name"], self.district.name)

    # ------------------ Setting ------------------
    def test_setting(self):
        url = reverse("common:setting")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["phone"], self.setting.phone)
        self.assertEqual(response.data["data"]["support_email"], self.setting.support_email)
        self.assertEqual(response.data["data"]["working_hours"], self.setting.working_hours)
        self.assertEqual(response.data["data"]["app_version"], self.setting.app_version)
        self.assertEqual(response.data["data"]["maintenance_mode"], self.setting.maintenance_mode)
