import uuid
from decimal import Decimal
from io import BytesIO

from accounts.models import CustomUser
from common.models import Region
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import translation
from PIL import Image
from rest_framework.test import APITestCase

from .models import Ad, Category, FavouriteProduct, MySearch, SearchCount


def generate_test_image():
    file = BytesIO()
    image = Image.new("RGB", (100, 100), "blue")
    image.save(file, "JPEG")
    file.seek(0)
    return SimpleUploadedFile("test.jpg", file.read(), content_type="image/jpeg")


class StoreAPITests(APITestCase):
    def setUp(self):
        super().setUp()
        Ad.objects.all().delete()
        MySearch.objects.all().delete()
        FavouriteProduct.objects.all().delete()
        Category.objects.all().delete()
        Category.objects.all().delete()

        self.parent_category = Category.objects.create(name_uz="Elektronika", name_ru="Техника")

        self.child_category = Category.objects.create(
            name_uz="Telefonlar", name_ru="Телефоны", parent=self.parent_category
        )
        self.region = Region.objects.create(name="Tashkent")
        self.user = CustomUser.objects.create_user(
            phone_number="998901112233", full_name="Test User", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        Ad.objects.create(
            name="telefon",
            category=self.child_category,
            description="Test description",
            price=3000000,
            seller=self.user,
        )

        Ad.objects.create(
            name="iPhone 11",
            category=self.child_category,
            description="Test description 2",
            price=5000000,
            seller=self.user,
        )

        MySearch.objects.all().delete()

    def test_categories_list(self):
        url = reverse("store:category-list")

        # Default til (uz)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"][0]["name"], self.parent_category.name_uz)

        # Rus tilida tekshirish
        response = self.client.get(url, HTTP_ACCEPT_LANGUAGE="ru")
        expected_name = self.parent_category.name_ru
        self.assertEqual(response.data["data"][0]["name"], expected_name)

    def test_categories_with_children(self):
        url = reverse("store:categories-with-children")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])

        with translation.override("ru"):
            response = self.client.get(url, HTTP_ACCEPT_LANGUAGE="ru")
            expected_child_name = self.child_category.name_ru
            self.assertEqual(response.data["data"][0]["children"][0]["name"], expected_child_name)

    def test_sub_category(self):
        url = reverse("store:sub-category-list")
        response = self.client.get(url, {"parent_id": self.parent_category.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])

        with translation.override("ru"):
            response = self.client.get(
                url, {"parent_id": self.parent_category.id}, HTTP_ACCEPT_LANGUAGE="ru"
            )
            expected_name = self.child_category.name_ru
            self.assertEqual(response.data["data"][0]["name"], expected_name)

    def test_create_ad(self):
        url = reverse("store:create-ads")
        image = generate_test_image()

        ad_data = {
            "name_uz": "telefon",
            "name_ru": "телефон",
            "description_uz": "Test description",
            "description_ru": "Тест описание",
            "category": self.child_category.id,
            "price": 21000,
            "photos": [image],
        }

        response = self.client.post(url, ad_data, format="multipart")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["name"], "telefon")
        self.assertEqual(response.data["data"]["seller"]["id"], self.user.id)
        self.assertEqual(response.data["data"]["seller"]["full_name"], "Test User")

    def test_get_ad_detail(self):
        create_url = reverse("store:create-ads")
        ad_data = {
            "name_uz": "iPhone 11",
            "name_ru": "Айфон 11",
            "description_uz": "Yangi iPhone",
            "description_ru": "Новый iPhone",
            "category": self.child_category.id,
            "price": "21000",
            "photos": generate_test_image(),
        }

        create_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(create_response.status_code, 201)

        slug = create_response.data["data"]["slug"]

        detail_url = reverse("store:detail-ad", kwargs={"slug": slug})
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["name"], ad_data["name_uz"])
        self.assertEqual(response.data["data"]["category"]["name"], self.child_category.name)
        self.assertEqual(response.data["data"]["seller"]["id"], self.user.id)

    def test_ads_list(self):
        url = reverse("store:list-ads")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIn("results", response.data["data"])
        self.assertIsInstance(response.data["data"]["results"], list)

    def test_create_favourite_product(self):
        create_url = reverse("store:create-ads")
        image = generate_test_image()
        ad_data = {
            "name_uz": "telefon",
            "name_ru": "телефон",
            "category": self.child_category.id,
            "description_uz": "test uz desc",
            "description_ru": "test ru desc",
            "price": "1000.00",
            "photos": [image],
        }
        ad_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(ad_response.status_code, 201)
        product_id = ad_response.data["data"]["id"]

        self.client.force_authenticate(user=None)

        url = reverse("store:favourite-product-create-by-id")
        data = {"device_id": "1234567890testdevice", "product": product_id}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["product"], product_id)
        self.assertEqual(response.data["data"]["device_id"], "1234567890testdevice")

    def test_get_favourite_products_by_device_id(self):
        create_url = reverse("store:create-ads")
        image = generate_test_image()
        ad_data = {
            "name_uz": "iPhone",
            "name_ru": "Айфон",
            "category": self.child_category.id,
            "description_uz": "uz desc",
            "description_ru": "test description",
            "price": 2145,
        }
        ad_response = self.client.post(
            create_url,
            {**ad_data, "photos": [image]},
            format="multipart",
        )

        self.assertEqual(ad_response.status_code, 201, ad_response.data)
        product_id = ad_response.data["data"]["id"]
        self.client.force_authenticate(user=None)
        fav_url = reverse("store:favourite-product-create-by-id")
        self.client.post(
            fav_url, {"device_id": "1234567890testdevice", "product": product_id}, format="json"
        )

        list_url = reverse("store:my-favourite-product-by-id")
        response = self.client.get(list_url, {"device_id": "1234567890testdevice"})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["count"], 1)
        self.assertEqual(response.data["data"]["results"][0]["id"], product_id)
        self.assertEqual(response.data["data"]["results"][0]["name"], "iPhone")

    def test_delete_favourite_product(self):
        create_url = reverse("store:create-ads")
        image = generate_test_image()
        ad_data = {
            "name_uz": "telefon",
            "name_ru": "телефон",
            "category": self.child_category.id,
            "description_uz": "test uz desc",
            "description_ru": "test ru desc",
            "price": "1000.00",
            "photos": [image],
        }
        ad_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(ad_response.status_code, 201)
        product_id = ad_response.data["data"]["id"]

        self.client.force_authenticate(user=None)

        fav_url = reverse("store:favourite-product-create-by-id")
        fav_data = {
            "device_id": "1234567890testdevice",
            "product": product_id,
        }
        fav_response = self.client.post(fav_url, fav_data, format="json")
        self.assertEqual(fav_response.status_code, 201)

        delete_url = reverse("store:favourite-product-delete-by-id", kwargs={"pk": product_id})
        delete_response = self.client.delete(f"{delete_url}?device_id=1234567890testdevice")

        self.assertIn(delete_response.status_code, [200, 204])
        if delete_response.status_code == 200:
            self.assertTrue(delete_response.data["success"])
        self.assertIsNone(delete_response.data["data"])

    def test_create_favourite_product_authenticated_user(self):
        create_url = reverse("store:create-ads")
        image = generate_test_image()
        ad_data = {
            "name_uz": "telefon",
            "name_ru": "телефон",
            "category": self.child_category.id,
            "description_uz": "test uz desc",
            "description_ru": "test ru desc",
            "price": "1000.00",
            "photos": [image],
        }
        ad_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(ad_response.status_code, 201)
        product_id = ad_response.data["data"]["id"]

        url = reverse("store:favourite-product-create")
        data = {"product": product_id}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["product"], product_id)
        self.assertNotIn("device_id", response.data["data"])

    def test_get_my_favourite_products_authenticated_user(self):
        Ad.objects.all().delete()
        FavouriteProduct.objects.all().delete()

        create_url = reverse("store:create-ads")

        # Required fieldlar va to'g'ri format
        ad_data = {
            "name_uz": "iPhone 11",
            "name_ru": "iPhone 11",
            "category": self.child_category.id,
            "description_uz": "test uz desc",
            "description_ru": "test description",
            "price": 2156,  # raqam
            "photos": generate_test_image(),  # SimpleUploadedFile list
            "region": self.region.id,
        }

        # Ad yaratish
        ad_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(ad_response.status_code, 201, ad_response.data)
        product_id = ad_response.data["data"]["id"]

        # Favourites ga qo'shish
        fav_url = reverse("store:favourite-product-create")
        fav_response = self.client.post(fav_url, {"product": product_id}, format="json")
        self.assertEqual(fav_response.status_code, 201, fav_response.data)

        # Favourites listni olish
        list_url = reverse("store:my-favourite-product")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["count"], 1)
        self.assertEqual(response.data["data"]["results"][0]["id"], product_id)
        self.assertEqual(response.data["data"]["results"][0]["name"], "iPhone 11")

    def test_delete_favourite_product_authenticated(self):
        create_url = reverse("store:create-ads")
        image = generate_test_image()
        ad_data = {
            "name_uz": "telefon",
            "name_ru": "телефон",
            "category": self.child_category.id,
            "description_uz": "test uz desc",
            "description_ru": "test ru desc",
            "price": "1000.00",
            "photos": [image],
        }
        ad_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(ad_response.status_code, 201)
        product_id = ad_response.data["data"]["id"]

        phone_number = "9989" + str(uuid.uuid4().int)[:7]
        user = CustomUser.objects.create_user(
            phone_number=phone_number,
            password="strongpassword",
        )
        self.client.force_authenticate(user=user)

        fav = FavouriteProduct.objects.create(user=user, product_id=product_id)

        delete_url = reverse("store:favourite-delete", kwargs={"pk": product_id})
        delete_response = self.client.delete(delete_url)

        self.assertEqual(delete_response.status_code, 204)
        self.assertTrue(delete_response.data["success"])
        self.assertIsNone(delete_response.data["data"])
        self.assertFalse(
            FavouriteProduct.objects.filter(id=fav.id).exists(),
            "Favorite Product is not removed from the database",
        )

    def test_my_ads_list_authenticated_user(self):
        create_url = reverse("store:create-ads")

        image1 = generate_test_image()
        ad_data1 = {
            "name_uz": "Телефон",
            "name_ru": "телефон",
            "category": self.child_category.id,
            "description_uz": "uz desc",
            "description_ru": "test desc",
            "price": "2.02",
            "photos": [image1],
            "address": "Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 16-uy",
        }
        self.client.post(create_url, ad_data1, format="multipart")

        image2 = generate_test_image()
        ad_data2 = {
            "name_uz": "vivo 53s",
            "name_ru": "vivo 53s",
            "category": self.child_category.id,
            "description_uz": "uz desc",
            "description_ru": "desc ru",
            "price": "3000000.00",
            "photos": [image2],
            "address": "Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 16-uy",
        }
        self.client.post(create_url, ad_data2, format="multipart")

        url = reverse("store:my-ads")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.data["success"])
        self.assertIn("results", response.data["data"])

        results = response.data["data"]["results"]
        self.assertGreaterEqual(len(results), 2)

        for ad in results:
            self.assertIn("id", ad)
            self.assertIn("name", ad)
            self.assertIn("price", ad)
            self.assertIn("status", ad)

    def test_my_ad_detail_authenticated_user(self):
        create_url = reverse("store:create-ads")
        image = generate_test_image()
        ad_data = {
            "name_uz": "vivo 53s",
            "name_ru": "vivo 53s",
            "category": self.child_category.id,
            "description_uz": "uz desc",
            "description_ru": "Smartphone VIVO 53s",
            "price": "3000000.00",
            "photos": [image],
            "address": "Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 16-uy",
        }
        create_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(create_response.status_code, 201)
        ad_id = create_response.data["data"]["id"]

        url = reverse("store:my-ad", kwargs={"pk": ad_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.data["success"])
        self.assertIn("id", response.data["data"])
        self.assertIn("name", response.data["data"])
        self.assertIn("description", response.data["data"])
        self.assertIn("category", response.data["data"])
        self.assertIn("price", response.data["data"])
        self.assertIn("photos", response.data["data"])
        self.assertIn("status", response.data["data"])
        self.assertIn("view_count", response.data["data"])

        self.assertEqual(response.data["data"]["id"], ad_id)

    def test_update_my_ad_put(self):
        self.client.force_authenticate(user=self.user)

        ad = Ad.objects.create(
            name="Old Ad",
            category=self.parent_category,
            description="Old description",
            price=1000,
            seller=self.user,
        )

        new_image = generate_test_image()
        data = {
            "name": "iPhone 15 Pro Max 256GB Titanium (Yangilangan)",
            "category": self.parent_category.id,
            "description": "...",
            "price": 14500000,
            "new_photos": [new_image],
        }

        url = reverse("store:my-ad", kwargs={"pk": ad.id})
        response = self.client.put(url, data, format="multipart")

        # Tekshirish
        self.assertEqual(response.status_code, 200, f"Unexpected response: {response.content}")
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["name"], data["name"])
        self.assertAlmostEqual(Decimal(response.data["data"]["price"]), Decimal(str(data["price"])))

    def test_update_my_ad_patch(self):
        ad = Ad.objects.create(
            name="Old Ad",
            category=self.parent_category,
            description="Old description",
            price=1000,
            seller=self.user,
        )

        self.client.force_authenticate(user=self.user)

        data = {"price": 2000}

        url = reverse("store:my-ad", kwargs={"pk": ad.id})
        response = self.client.patch(url, data, format="json")  # << PATCH ishlatamiz

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertAlmostEqual(Decimal(response.data["data"]["price"]), Decimal(str(data["price"])))
        self.assertEqual(response.data["data"]["name"], "Old Ad")  # unchanged

    def test_delete_my_ad(self):
        create_url = reverse("store:create-ads")
        image = generate_test_image()
        ad_data = {
            "name_uz": "Delete test",
            "name_ru": "Delete test",
            "category": self.child_category.id,
            "description_uz": "uz desc",
            "description_ru": "to be deleted",
            "price": "5000000.00",
            "photos": [image],
            "address": "Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 16-uy",
        }
        create_response = self.client.post(create_url, ad_data, format="multipart")
        self.assertEqual(create_response.status_code, 201)
        ad_id = create_response.data["data"]["id"]

        delete_url = reverse("store:my-ad", kwargs={"pk": ad_id})
        response = self.client.delete(delete_url)

        self.assertIn(response.status_code, [200, 204])
        self.assertTrue(response.data["success"])
        self.assertIsNone(response.data["data"])

    def test_product_download_by_slug(self):
        ad = Ad.objects.create(
            name="iPhone 11",
            category=self.child_category,
            description="test description",
            price=214,
            seller=self.user,
        )

        slug = ad.slug

        url = reverse("store:product-download", kwargs={"slug": slug})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.data["success"])
        data = response.data["data"]
        self.assertEqual(data["id"], ad.id)
        self.assertEqual(data["name"], ad.name)
        self.assertEqual(data["slug"], ad.slug)
        self.assertEqual(data["description"], ad.description)
        self.assertAlmostEqual(float(data["price"]), float(ad.price), places=2)
        self.assertEqual(data["category"]["id"], self.child_category.id)
        self.assertEqual(data["category"]["name"], self.child_category.name)
        self.assertEqual(data["seller"]["id"], self.user.id)
        self.assertEqual(data["seller"]["full_name"], self.user.full_name)

    def test_create_product_image(self):
        ad = Ad.objects.create(
            name="iPhone 11",
            category=self.child_category,
            description="test description",
            price=21.45,
            seller=self.user,
        )

        url = reverse("store:product-image-create")
        image = generate_test_image()
        data = {
            "image": image,
            "is_main": True,
            "product_id": ad.id,
        }

        response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])

        data_resp = response.data["data"]
        self.assertEqual(data_resp["product_id"], ad.id)
        self.assertEqual(data_resp["is_main"], True)
        self.assertIn("image", data_resp)
        self.assertIn("id", data_resp)
        self.assertIn("created_at", data_resp)

    def test_category_product_search_by_query(self):
        Category.objects.create(name="Техника")
        Category.objects.create(name="Смартфоны")

        url = reverse("store:category-product-search")
        response = self.client.get(url, {"q": "Техника"})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIsInstance(response.data["data"], list)
        self.assertEqual(response.data["data"][0]["name"], "Техника")

    def test_complete_search_by_query(self):
        Ad.objects.create(
            name_uz="vivo 53s",
            name_ru="vivo 53s",
            description_uz="test description uz",
            description_ru="test description ru",
            category=self.child_category,
            price=3000000,
            seller=self.user,
        )

        Ad.objects.create(
            name_uz="iPhone 11",
            name_ru="iPhone 11",
            description_uz="Test tavsifi",
            description_ru="Тестовое описание",
            category=self.child_category,
            price=21000000,
            seller=self.user,
        )

        url = reverse("store:search-complete")

        # Request'ga tilni header orqali beramiz
        response = self.client.get(url, {"q": "vivo"}, HTTP_ACCEPT_LANGUAGE="uz")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIsInstance(response.data["data"], list)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["name"], "vivo 53s")

    def test_search_count_increase(self):
        ad = Ad.objects.create(
            name="vivo 53s",
            category=self.child_category,
            description="test description",
            price=3000000,
            seller=self.user,
        )

        search_count_obj = SearchCount.objects.create(product=ad, search_count=0)

        url = reverse("store:search-count", kwargs={"category_id": ad.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIn("data", response.data)

        data = response.data["data"]
        self.assertEqual(data["id"], ad.id)
        self.assertEqual(data["category"], ad.category.id)
        self.assertEqual(data["search_count"], 1)
        self.assertIn("updated_at", data)

        search_count_obj.refresh_from_db()
        self.assertEqual(search_count_obj.search_count, 1)

    def test_search_populars(self):
        ad1 = Ad.objects.create(
            name="vivo 53s",
            category=self.child_category,
            description="desc",
            price=3000000,
            seller=self.user,
        )
        ad2 = Ad.objects.create(
            name="test ru name",
            category=self.child_category,
            description="desc",
            price=1500000,
            seller=self.user,
        )

        SearchCount.objects.create(product=ad1, search_count=4)
        SearchCount.objects.create(product=ad2, search_count=1)

        url = reverse("store:popular-searches")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIn("data", response.data)
        self.assertIsInstance(response.data["data"], list)
        results = response.data["data"]

        self.assertGreaterEqual(len(results), 2)

        for item in results:
            self.assertIn("id", item)
            self.assertIn("name", item)
            self.assertIn("icon", item)
            self.assertIn("search_count", item)

        self.assertEqual(results[0]["search_count"], 4)
        self.assertEqual(results[1]["search_count"], 1)

    def test_create_my_search(self):
        category = Category.objects.create(name="Texnika")

        from common.models import Region

        region = Region.objects.create(name="Tashkent")

        url = reverse("store:my-search-create")
        data = {
            "category": category.id,
            "search_query": "iPhone",
            "price_min": "1000000.00",
            "price_max": "20000000.00",
            "region_id": region.id,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["success"])

    def test_my_search_list(self):
        # Category va region yaratish
        category = Category.objects.create(name_uz="Smartphones", name_ru="Смартфоны")
        region = Region.objects.create(name="Tashkent")

        # MySearch yaratish
        my_search = MySearch.objects.create(
            user=self.user,
            category=category,
            search_query="iPhone",
            price_min=1000000,
            price_max=20000000,
            region=region,
        )

        # API chaqirish (tilni header orqali beramiz)
        url = reverse("store:my-search-list")
        response = self.client.get(url, HTTP_ACCEPT_LANGUAGE="uz")

        # Javobni tekshirish
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])
        self.assertIn("data", response.data)

        results = response.data["data"]
        self.assertEqual(len(results), 1)

        search_data = results[0]

        # Asosiy maydonlar
        self.assertEqual(search_data["id"], my_search.id)
        self.assertEqual(search_data["category"]["id"], category.id)
        self.assertEqual(search_data["search_query"], "iPhone")

        # Decimal/float moslash
        self.assertEqual(int(search_data["price_min"]), 1000000)
        self.assertEqual(int(search_data["price_max"]), 20000000)

        # Region chiqishi serializerga qarab tekshiriladi
        if "region_id" in search_data:
            self.assertEqual(search_data["region_id"], region.id)
        elif "region" in search_data:
            self.assertEqual(search_data["region"]["id"], region.id)

        self.assertIn("created_at", search_data)

    def test_delete_my_search(self):
        category = Category.objects.create(name="Smartphones")
        region = Region.objects.create(name="Tashkent")

        my_search = MySearch.objects.create(
            user=self.user,
            category=category,
            search_query="iPhone",
            price_min=1000000,
            price_max=20000000,
            region_id=region.id,
        )

        url = reverse("store:my-search-delete", kwargs={"pk": my_search.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertTrue(response.data["success"])
        self.assertIsNone(response.data["data"])

        self.assertFalse(MySearch.objects.filter(id=my_search.id).exists())
