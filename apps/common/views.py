from rest_framework import generics
from .models import Page
from .serializers import PageListSerializer, PageDetailSerializer

class PageListAPIView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer

class PageDetailAPIView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    lookup_field = 'slug'
