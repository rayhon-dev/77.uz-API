from rest_framework import generics
from .models import Page, Region, Setting
from .pagination import CustomPagination
from .serializers import PageListSerializer, PageDetailSerializer, RegionSerializer, SettingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class PageListAPIView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer
    pagination_class = CustomPagination

class PageDetailAPIView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    lookup_field = 'slug'


class RegionWithDistrictsView(APIView):
    def get(self, request):
        regions = Region.objects.prefetch_related('districts').all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)


class SettingView(APIView):
    def get(self, request):
        setting = Setting.objects.first()
        serializer = SettingSerializer(setting)
        return Response(serializer.data)
