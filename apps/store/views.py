from common.utils.custom_response_decorator import custom_response
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from .models import Ad, Category
from .openapi_schema import (
    ad_create_response,
    ad_create_schema,
    ad_detail_response,
    categories_with_children_response,
    category_list_response,
)
from .permissions import IsSeller
from .serializers import (
    AdCreateSerializer,
    AdDetailSerializer,
    CategorySerializer,
    CategoryWithChildrenSerializer,
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
        operation_description="Returns full detail of an ad by slug",
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
