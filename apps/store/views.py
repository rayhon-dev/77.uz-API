from common.utils.custom_response_decorator import custom_response
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from .models import Ad, Category, FavouriteProduct
from .openapi_schema import (
    ad_create_response,
    ad_create_schema,
    ad_detail_response,
    categories_with_children_response,
    category_list_response,
    favourite_product_auth_response,
    favourite_product_create_by_id_request,
    favourite_product_create_request,
    favourite_product_delete_response,
    favourite_product_response,
)
from .permissions import IsSeller
from .serializers import (
    AdCreateSerializer,
    AdDetailSerializer,
    CategorySerializer,
    CategoryWithChildrenSerializer,
    FavouriteProductCreateByIdSerializer,
    FavouriteProductCreateSerializer,
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


class FavouriteProductCreateByIdView(generics.CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductCreateByIdSerializer

    @swagger_auto_schema(
        operation_summary="Add a favourite product by device_id",
        operation_description="Allows a guest user to add a product to favourites by providing a device_id.",
        request_body=favourite_product_create_by_id_request,
        responses={201: favourite_product_response, 400: "Validation error"},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class FavouriteProductDeleteByIdView(generics.DestroyAPIView):
    queryset = FavouriteProduct.objects.all()

    @swagger_auto_schema(
        operation_summary="Delete a favourite product by device_id",
        operation_description="Deletes a favourite product entry for a guest user based on device_id and product ID.",
        responses={204: favourite_product_delete_response, 404: "Not found"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        device_id = self.request.query_params.get("device_id")
        if not device_id:
            raise PermissionDenied("device_id parameter majburiy.")
        return FavouriteProduct.objects.filter(device_id=device_id)


class FavouriteProductCreateView(generics.CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductCreateSerializer
    permission_classes = [IsSeller]

    @swagger_auto_schema(
        operation_summary="Add a favourite product (authenticated user)",
        operation_description="Allows an authenticated user to add a product to favourites by product ID.",
        request_body=favourite_product_create_request,
        responses={201: favourite_product_auth_response, 400: "Validation error"},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class FavouriteProductDeleteView(generics.DestroyAPIView):
    queryset = FavouriteProduct.objects.all()
    permission_classes = [IsSeller]

    @swagger_auto_schema(
        operation_summary="Delete a favourite product (authenticated user)",
        operation_description="Deletes a favourite product entry for the authenticated user.",
        responses={204: favourite_product_delete_response, 404: "Not found"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return FavouriteProduct.objects.filter(user=self.request.user)
