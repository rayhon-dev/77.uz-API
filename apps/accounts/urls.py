from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import path
from .views import SellerRegistrationView, CustomLoginView, CustomTokenVerifyView


urlpatterns = [
    path('seller/registration/', SellerRegistrationView.as_view(), name='register-seller'),
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
]