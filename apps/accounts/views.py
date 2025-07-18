from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SellerRegistrationSerializer


class SellerRegistrationView(APIView):
    def post(self, request):
        serializer = SellerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            user.is_active = False
            user.is_approved = False
            user.save()

            return Response({
                "message": "Arizangiz qabul qilindi. Admin siz bilan tez orada bog‘lanadi."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
