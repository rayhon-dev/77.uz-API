from django.urls import path

from .views import PageDetailAPIView, PageListAPIView, RegionWithDistrictsView, SettingView

urlpatterns = [
    path("pages/", PageListAPIView.as_view()),
    path("pages/<slug:slug>/", PageDetailAPIView.as_view()),
    path("regions-with-districts/", RegionWithDistrictsView.as_view()),
    path("setting/", SettingView.as_view()),
]
