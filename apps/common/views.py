from rest_framework import generics
from .models import Page
from .pagination import CustomPagination
from .serializers import PageListSerializer, PageDetailSerializer

class PageListAPIView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer
    pagination_class = CustomPagination

class PageDetailAPIView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    lookup_field = 'slug'
