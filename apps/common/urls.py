from django.urls import path
from .views import PageListAPIView, PageDetailAPIView

urlpatterns = [
    path('common/pages/', PageListAPIView.as_view()),
    path('common/pages/<slug:slug>/', PageDetailAPIView.as_view()),
]
