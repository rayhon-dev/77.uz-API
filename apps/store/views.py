from common.pagination import (
    AdListPagination,
    MyAdsListPagination,
    MyFavouriteProductPagination,
    MySearchPagination,
)
from common.utils.custom_response_decorator import custom_response
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .filters import AdFilter
from .models import Ad, AdPhoto, Category, FavouriteProduct, MySearch, SearchCount
from .openapi_schema import (
    ad_create_response,
    ad_create_schema,
    ad_detail_response,
    ad_list_parameters,
    ad_list_response,
    ad_photo_create_request,
    ad_photo_create_response,
    categories_with_children_response,
    category_list_response,
    favourite_product_guest_request,
    favourite_product_response,
    favourite_product_response_for_seller,
    favourite_product_seller_request,
    my_ad_detail_response,
    my_ad_update_request,
    my_ad_update_response,
    my_ads_list_response,
    my_favourite_products_response,
    my_search_create_request,
    my_search_create_response,
    my_search_list_response,
    popular_search_response,
    search_complete_response,
    search_count_response,
    search_product_response,
    sub_category_list_response,
)
from .permissions import IsSeller
from .serializers import (
    AdCreateSerializer,
    AdDetailSerializer,
    AdListSerializer,
    AdPhotoSerializer,
    CategorySerializer,
    CategoryWithChildrenSerializer,
    FavouriteProductListSerializer,
    FavouriteProductSerializer,
    MyAdsDetailSerializer,
    MyAdsListSerializer,
    MySearchCreateSerializer,
    MySearchSerializer,
    PopularSearchSerializer,
    SearchCategorySerializer,
    SearchCompleteSerializer,
    SearchCountSerializer,
    SearchProductSerializer,
    SubCategorySerializer,
)


@custom_response
class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    permission_classes = [IsSeller]

    @swagger_auto_schema(
        operation_summary="Create a new ad",
        operation_description="Allows an authenticated seller to create a new advertisement with images.",
        request_body=ad_create_schema,
        responses={201: ad_create_response, 400: "Validation error"},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@custom_response
class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    lookup_field = "slug"

    @swagger_auto_schema(
        operation_summary="Get ad details",
        operation_description="Returns full detail of an ad by slug.",
        responses={200: ad_detail_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class CategoriesWithChildrenView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategoryWithChildrenSerializer

    @swagger_auto_schema(
        operation_summary="Get parent categories with children",
        operation_description="Returns a list of top-level categories including their child categories.",
        responses={200: categories_with_children_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        operation_summary="List all categories",
        operation_description="Returns all categories along with the number of ads in each category.",
        responses={200: category_list_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Category.objects.annotate(product_count=Count("ad"))


@custom_response
class FavouriteProductCreateView(generics.CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer
    permission_classes = [IsSeller]

    @swagger_auto_schema(
        operation_summary="Add product to favourites (Seller)",
        operation_description="Authorized sellers can add products to favourites by providing product ID.",
        request_body=favourite_product_seller_request,
        responses={201: favourite_product_response_for_seller, 400: "Validation Error"},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@custom_response
class FavouriteProductCreateByIDView(generics.CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer

    @swagger_auto_schema(
        operation_summary="Add product to favourites (Guest)",
        operation_description="Guests must provide both product ID and device ID.",
        request_body=favourite_product_guest_request,
        responses={201: favourite_product_response, 400: "Validation Error"},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        device_id = self.request.data.get("device_id")
        if not device_id:
            raise serializers.ValidationError({"device_id": "This field is required."})
        serializer.save(device_id=device_id)


@custom_response
class FavouriteProductDeleteView(generics.DestroyAPIView):
    serializer_class = FavouriteProductSerializer
    permission_classes = [IsSeller]

    def get_queryset(self):
        return FavouriteProduct.objects.filter(user=self.request.user)

    def get_object(self):
        product_id = self.kwargs["pk"]
        return self.get_queryset().get(product_id=product_id)

    @swagger_auto_schema(
        operation_summary="Delete favourite product (Seller)",
        operation_description="Deletes a product from the authenticated seller's favourite list using the product ID.",
        responses={204: openapi.Response(description="Successfully deleted")},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


@custom_response
class FavouriteProductDeleteByIDView(generics.DestroyAPIView):
    serializer_class = FavouriteProductSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return FavouriteProduct.objects.none()

        device_id = self.request.query_params.get("device_id")
        if not device_id:
            raise serializers.ValidationError(
                {"device_id": "This field is required in query parameters."}
            )
        return FavouriteProduct.objects.filter(device_id=device_id)

    def get_object(self):
        product_id = self.kwargs["pk"]
        return self.get_queryset().get(product_id=product_id)

    @swagger_auto_schema(
        operation_summary="Delete favourite product (Guest)",
        operation_description=(
            "Deletes a product from guest favourites using the product ID. "
            "Requires `device_id` to be passed in query parameters."
        ),
        responses={204: openapi.Response(description="Successfully deleted")},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


@custom_response
class AdListView(generics.ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer
    pagination_class = AdListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AdFilter
    search_fields = ["name"]
    ordering_fields = ["published_at", "price", "view_count"]
    ordering = ["-published_at"]

    @swagger_auto_schema(
        operation_summary="List of ads",
        operation_description="Returns a paginated list of ads. Supports filtering, search, and ordering.",
        manual_parameters=ad_list_parameters,
        responses={200: openapi.Response("List of Ads", ad_list_response)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class MyAdsListAPIView(generics.ListAPIView):
    serializer_class = MyAdsListSerializer
    permission_classes = [IsSeller]
    filterset_fields = ["status"]
    pagination_class = MyAdsListPagination

    def get_queryset(self):
        user = self.request.user
        return Ad.objects.filter(seller=user).order_by("-published_at")

    @swagger_auto_schema(
        operation_summary="List My Ads",
        operation_description="Get a paginated list of ads created by the authenticated seller. Supports filtering by `status`.",
        responses={200: my_ads_list_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class MyAdDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MyAdsDetailSerializer
    permission_classes = [IsSeller]
    lookup_field = "pk"

    def get_queryset(self):
        return Ad.objects.filter(seller=self.request.user)

    @swagger_auto_schema(
        operation_summary="Retrieve My Ad",
        operation_description="Get detailed information about a specific ad belonging to the authenticated seller.",
        responses={200: my_ad_detail_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update My Ad",
        operation_description="Update fields of an ad. Existing photos are replaced if `new_photos` is provided.",
        request_body=my_ad_update_request,
        responses={200: my_ad_update_response},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update My Ad",
        operation_description="Partially update specific fields of an ad. Only the fields provided in the request will be updated.",
        request_body=my_ad_update_request,
        responses={200: my_ad_update_response},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete My Ad",
        operation_description="Delete a specific ad belonging to the authenticated seller.",
        responses={204: "No Content"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


@custom_response
class MyFavouriteProductView(generics.ListAPIView):
    serializer_class = FavouriteProductListSerializer
    pagination_class = MyFavouriteProductPagination
    permission_classes = [IsSeller]

    def get_queryset(self):
        category_id = self.request.query_params.get("category")
        queryset = FavouriteProduct.objects.filter(user=self.request.user)
        if category_id:
            queryset = queryset.filter(product__category_id=category_id)
        return (
            queryset.select_related("product", "product__seller")
            .prefetch_related("product__photos")
            .order_by("-id")
        )

    @swagger_auto_schema(
        operation_summary="List My Favourite Products",
        operation_description="Get a paginated list of favourite products of the authenticated user. Can filter by category using `category` query parameter.",
        manual_parameters=[
            openapi.Parameter(
                "category",
                openapi.IN_QUERY,
                description="Filter by category ID",
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={200: my_favourite_products_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class MyFavouriteProductByIdView(generics.ListAPIView):
    serializer_class = FavouriteProductListSerializer
    pagination_class = MyFavouriteProductPagination

    def get_queryset(self):
        device_id = self.request.query_params.get("device_id")
        return (
            FavouriteProduct.objects.filter(device_id=device_id)
            .select_related("product", "product__seller")
            .prefetch_related("product__photos")
            .order_by("-id")
        )

    def list(self, request, *args, **kwargs):
        device_id = request.query_params.get("device_id")
        if not device_id:
            raise ValidationError({"device_id": "This field is required in query parameters."})
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="List Favourite Products by Device ID",
        operation_description="Get a paginated list of favourite products linked to a device. Requires `device_id` in query parameters.",
        manual_parameters=[
            openapi.Parameter(
                "device_id",
                openapi.IN_QUERY,
                description="Device ID to filter favourites",
                required=True,
                type=openapi.TYPE_STRING,
            )
        ],
        responses={200: my_favourite_products_response},  # openapi_schema.py dagi response
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class MySearchCreateView(generics.CreateAPIView):
    queryset = MySearch.objects.all()
    serializer_class = MySearchCreateSerializer
    permission_classes = [IsSeller]

    @swagger_auto_schema(
        operation_summary="Create a Search Entry",
        operation_description="Allows the authenticated seller to create a new search entry for tracking purposes.",
        request_body=my_search_create_request,  # agar openapi_schema.py da buni yaratgan bo'lsangiz
        responses={201: my_search_create_response},  # openapi_schema.py dagi response
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@custom_response
class MySearchListView(generics.ListAPIView):
    serializer_class = MySearchSerializer
    pagination_class = MySearchPagination
    permission_classes = [IsSeller]

    @swagger_auto_schema(
        operation_summary="List My Searches",
        operation_description="Returns a paginated list of searches performed by the authenticated seller.",
        responses={200: my_search_list_response},  # openapi_schema.py dagi response
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return MySearch.objects.filter(user=self.request.user).order_by("-created_at")


@custom_response
class MySearchDeleteView(generics.DestroyAPIView):
    queryset = MySearch.objects.all()
    permission_classes = [IsSeller]

    @swagger_auto_schema(
        operation_summary="Delete My Search Entry",
        operation_description="Deletes a search entry belonging to the authenticated seller.",
        responses={204: "No Content"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return MySearch.objects.filter(user=self.request.user)


@custom_response
class ProductDownloadView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    lookup_field = "slug"

    @swagger_auto_schema(
        operation_summary="Download Product Details",
        operation_description="Retrieve detailed information of a product using its slug.",
        responses={200: ad_detail_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class ProductImageCreateView(generics.CreateAPIView):
    serializer_class = AdPhotoSerializer
    queryset = AdPhoto.objects.all()
    permission_classes = [IsSeller]

    @swagger_auto_schema(
        operation_summary="Upload Product Images",
        operation_description="Allows the authenticated seller to upload images for their products.",
        request_body=ad_photo_create_request,
        responses={201: ad_photo_create_response},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@custom_response
class CategoryProductSearchView(generics.ListAPIView):
    serializer_class = SearchProductSerializer  # swagger uchun default

    def get_queryset(self):
        q = self.request.query_params.get("q", "")
        categories = list(Category.objects.filter(name__icontains=q))
        products = list(
            Ad.objects.filter(Q(name__icontains=q) | Q(description__icontains=q), status="active")
        )
        return categories + products

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        results = []

        for obj in queryset:
            if isinstance(obj, Category):
                results.append(
                    SearchCategorySerializer(obj, context=self.get_serializer_context()).data
                )
            else:
                results.append(
                    SearchProductSerializer(obj, context=self.get_serializer_context()).data
                )
        return Response(results)

    @swagger_auto_schema(
        operation_summary="Search Products and Categories",
        operation_description="Search for products and categories by a query string `q`. Returns a combined list of matching categories and products.",
        manual_parameters=[
            openapi.Parameter(
                "q",
                openapi.IN_QUERY,
                description="Search query string",
                required=False,
                type=openapi.TYPE_STRING,
            )
        ],
        responses={200: search_product_response},  # openapi_schema.py dagi response
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class SearchCompleteView(generics.ListAPIView):
    serializer_class = SearchCompleteSerializer

    def get_queryset(self):
        q = self.request.query_params.get("q", "")
        return Ad.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q), status="active"
        ).order_by("name")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        results = SearchCompleteSerializer(queryset, many=True).data
        return Response(results)

    @swagger_auto_schema(
        operation_summary="Search Autocomplete",
        operation_description="Provides a list of products matching the search query `q` for autocomplete suggestions.",
        manual_parameters=[
            openapi.Parameter(
                "q",
                openapi.IN_QUERY,
                description="Search query string",
                required=False,
                type=openapi.TYPE_STRING,
            )
        ],
        responses={200: search_complete_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class SearchCountIncreaseView(generics.RetrieveAPIView):
    serializer_class = SearchCountSerializer
    queryset = Ad.objects.all()

    def get_object(self):
        product_id = self.kwargs["category_id"]
        product = get_object_or_404(Ad, id=product_id)

        search_count, created = SearchCount.objects.get_or_create(product=product)
        search_count.search_count += 1
        search_count.save()

        return search_count

    @swagger_auto_schema(
        operation_summary="Increase Category Search Count",
        operation_description="Increment the search count for a category by its ID.",
        manual_parameters=[
            openapi.Parameter(
                "category_id",
                openapi.IN_PATH,
                description="ID of the category to increment search count",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        responses={200: search_count_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class PopularsView(generics.ListAPIView):
    serializer_class = PopularSearchSerializer

    def get_queryset(self):
        return SearchCount.objects.select_related("product").order_by("-search_count")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        results = PopularSearchSerializer(queryset, many=True).data
        return Response(results)

    @swagger_auto_schema(
        operation_summary="List Popular Products",
        operation_description="Returns a list of products ordered by the number of searches in descending order.",
        responses={200: popular_search_response},  # openapi_schema.py dagi response
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class SubCategoryListView(generics.ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        parent_id = self.request.query_params.get("parent__id")
        if parent_id:
            return Category.objects.filter(parent_id=parent_id)
        return Category.objects.filter(parent__isnull=False)

    @swagger_auto_schema(
        operation_summary="List Subcategories",
        operation_description="Returns a list of subcategories. Can filter by parent category using `parent__id` query parameter.",
        manual_parameters=[
            openapi.Parameter(
                "parent__id",
                openapi.IN_QUERY,
                description="Parent category ID to filter subcategories",
                required=False,
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={200: sub_category_list_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
