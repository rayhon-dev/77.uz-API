from rest_framework import generics

from .models import Page, Region, Setting
from .pagination import CustomPagination
from .serializers import (
    PageDetailSerializer,
    PageListSerializer,
    RegionSerializer,
    SettingSerializer,
)
from .utils.custom_response_decorator import custom_response


@custom_response
class PageListAPIView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer
    pagination_class = CustomPagination


@custom_response
class PageDetailAPIView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    lookup_field = "slug"


@custom_response
class RegionWithDistrictsView(generics.ListAPIView):
    queryset = Region.objects.prefetch_related("districts").all()
    serializer_class = RegionSerializer


@custom_response
class SettingView(generics.RetrieveAPIView):
    serializer_class = SettingSerializer

    def get_object(self):
        return Setting.objects.first()
