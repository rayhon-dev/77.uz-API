from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import SellerRegistrationSerializer
from .models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenVerifySerializer,
    UserMeSerializer
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from common.utils.custom_response_decorator import custom_response
from rest_framework import generics, permissions
from .serializers import UserUpdateSerializer


@custom_response
class SellerRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SellerRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # 'status', 'role', va 'is_active' create() ichida belgilangan
        return Response(
            {"message": "Arizangiz qabul qilindi. Admin siz bilan tez orada bog‘lanadi."},
            status=status.HTTP_201_CREATED
        )


@custom_response
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@custom_response
class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer


@custom_response
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)



@custom_response
class UserEditView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
