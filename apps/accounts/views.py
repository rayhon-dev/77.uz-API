from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import SellerRegistrationSerializer
from .models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenVerifyView
from .serializers import CustomTokenVerifySerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserMeSerializer



class SellerRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SellerRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user.is_active = False
        user.is_approved = False
        user.save()

        return Response({
            "message": "Arizangiz qabul qilindi. Admin siz bilan tez orada bog‘lanadi."
        }, status=status.HTTP_201_CREATED)



class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer




class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)
