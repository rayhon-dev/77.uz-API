from django.urls import path
from .views import PageListAPIView, PageDetailAPIView, RegionWithDistrictsView, SettingView

urlpatterns = [
    path('common/pages/', PageListAPIView.as_view()),
    path('common/pages/<slug:slug>/', PageDetailAPIView.as_view()),
    path('common/regions-with-districts/', RegionWithDistrictsView.as_view()),
    path('common/setting/', SettingView.as_view()),
]
