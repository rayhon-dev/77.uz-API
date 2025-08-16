from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from .models import Page, Region, Setting
from .openapi_schema import (
    page_detail_response,
    page_list_response,
    region_with_districts_response,
    setting_response,
)
from .pagination import PageListPagination
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
    pagination_class = PageListPagination

    @swagger_auto_schema(
        operation_summary="List pages",
        operation_description="Get a paginated list of pages.",
        responses={200: page_list_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class PageDetailAPIView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    lookup_field = "slug"

    @swagger_auto_schema(
        operation_summary="Retrieve page details",
        operation_description="Get full details of a single page by its slug.",
        responses={200: page_detail_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class RegionWithDistrictsView(generics.ListAPIView):
    queryset = Region.objects.prefetch_related("districts").all()
    serializer_class = RegionSerializer

    @swagger_auto_schema(
        operation_summary="List regions with districts",
        operation_description="Get all regions and their related districts.",
        responses={200: region_with_districts_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class SettingView(generics.RetrieveAPIView):
    serializer_class = SettingSerializer

    @swagger_auto_schema(
        operation_summary="Get site settings",
        operation_description="Retrieve the site settings configuration.",
        responses={200: setting_response},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return Setting.objects.first()
