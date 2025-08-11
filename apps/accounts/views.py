from common.utils.custom_response_decorator import custom_response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .models import CustomUser
from .openapi_schema import (
    edit_request,
    edit_response,
    login_request,
    login_response,
    me_response,
    seller_registration_request,
    seller_registration_response,
    token_refresh_request,
    token_refresh_response,
    token_verify_request,
    token_verify_response,
)
from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenVerifySerializer,
    SellerRegistrationSerializer,
    UserMeSerializer,
    UserUpdateSerializer,
)


@custom_response
class SellerRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SellerRegistrationSerializer

    @swagger_auto_schema(
        operation_summary="Seller Registration",
        request_body=seller_registration_request,
        responses={201: seller_registration_response},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@custom_response
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_summary="User Login", request_body=login_request, responses={200: login_response}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        operation_summary="Refresh JWT Token",
        request_body=token_refresh_request,
        responses={200: token_refresh_response},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@custom_response
class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer

    @swagger_auto_schema(
        operation_summary="Verify JWT Token",
        request_body=token_verify_request,
        responses={200: token_verify_response},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@custom_response
class MeView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserMeSerializer

    @swagger_auto_schema(operation_summary="Get Current User Info", responses={200: me_response})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


@custom_response
class UserEditView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Edit Current User Info (PUT)",
        request_body=edit_request,
        responses={200: edit_response},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially Edit Current User Info (PATCH)",
        request_body=edit_request,
        responses={200: edit_response},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
