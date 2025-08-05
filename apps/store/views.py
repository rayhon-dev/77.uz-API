from common.utils.custom_response_decorator import custom_response
from rest_framework import generics

from .models import Ad
from .permissions import IsSeller
from .serializers import AdCreateSerializer, AdDetailSerializer


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
