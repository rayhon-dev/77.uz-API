from common.pagination import (
    AdListPagination,
    MyAdsListPagination,
    MyFavouriteProductPagination,
    MySearchPagination,
)
from common.utils.custom_response_decorator import custom_response
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter

from .filters import AdFilter
from .models import Ad, AdPhoto, Category, FavouriteProduct, MySearch
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


@custom_response
class FavouriteProductCreateView(generics.CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer
    permission_classes = [IsSeller]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@custom_response
class FavouriteProductCreateByIDView(generics.CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer

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


@custom_response
class FavouriteProductDeleteByIDView(generics.DestroyAPIView):
    serializer_class = FavouriteProductSerializer

    def get_queryset(self):
        device_id = self.request.query_params.get("device_id")
        if not device_id:
            raise serializers.ValidationError(
                {"device_id": "This field is required in query parameters."}
            )
        return FavouriteProduct.objects.filter(device_id=device_id)

    def get_object(self):
        product_id = self.kwargs["pk"]
        return self.get_queryset().get(product_id=product_id)


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


@custom_response
class MyAdsListAPIView(generics.ListAPIView):
    serializer_class = MyAdsListSerializer
    permission_classes = [IsSeller]
    filterset_fields = ["status"]
    pagination_class = MyAdsListPagination

    def get_queryset(self):
        user = self.request.user
        return Ad.objects.filter(seller=user).order_by("-published_at")


@custom_response
class MyAdDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MyAdsDetailSerializer
    permission_classes = [IsSeller]
    lookup_field = "pk"

    def get_queryset(self):
        return Ad.objects.filter(seller=self.request.user)


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
            queryset.select_related("product", "product__seller", "product__address")
            .prefetch_related("product__photos")
            .order_by("-id")
        )


@custom_response
class MyFavouriteProductByIdView(generics.ListAPIView):
    serializer_class = FavouriteProductListSerializer
    pagination_class = MyFavouriteProductPagination

    def get_queryset(self):
        device_id = self.request.query_params.get("device_id")
        return (
            FavouriteProduct.objects.filter(device_id=device_id)
            .select_related("product", "product__seller", "product__address")
            .prefetch_related("product__photos")
            .order_by("-id")
        )

    def list(self, request, *args, **kwargs):
        device_id = request.query_params.get("device_id")
        if not device_id:
            raise ValidationError({"device_id": "This field is required in query parameters."})
        return super().list(request, *args, **kwargs)


@custom_response
class MySearchCreateView(generics.CreateAPIView):
    queryset = MySearch.objects.all()
    serializer_class = MySearchCreateSerializer
    permission_classes = [IsSeller]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@custom_response
class MySearchListView(generics.ListAPIView):
    serializer_class = MySearchSerializer
    pagination_class = MySearchPagination
    permission_classes = [IsSeller]

    def get_queryset(self):
        return MySearch.objects.filter(user=self.request.user).order_by("-created_at")


@custom_response
class MySearchDeleteView(generics.DestroyAPIView):
    queryset = MySearch.objects.all()
    permission_classes = [IsSeller]

    def get_queryset(self):
        return MySearch.objects.filter(user=self.request.user)


@custom_response
class ProductDownloadView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    lookup_field = "slug"


@custom_response
class ProductImageCreateView(generics.CreateAPIView):
    queryset = AdPhoto.objects.all()
    serializer_class = AdPhotoSerializer
    permission_classes = [IsSeller]
