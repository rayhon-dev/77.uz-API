from common.utils.custom_response_decorator import custom_response
from django.db.models import Count
from rest_framework import generics

from .models import Ad, Category
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


@custom_response
class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    lookup_field = "slug"


@custom_response
class CategoriesWithChildrenView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategoryWithChildrenSerializer


@custom_response
class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.annotate(product_count=Count("ad"))
