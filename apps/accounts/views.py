from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import SellerRegistrationSerializer
from .models import CustomUser


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
