from django.urls import path

from .views import PageDetailAPIView, PageListAPIView, RegionWithDistrictsView, SettingView

urlpatterns = [
    path("pages/", PageListAPIView.as_view(), name="pages-list"),
    path("pages/<slug:slug>/", PageDetailAPIView.as_view(), name="pages-detail"),
    path(
        "regions-with-districts/", RegionWithDistrictsView.as_view(), name="regions-with-districts"
    ),
    path("setting/", SettingView.as_view(), name="setting"),
]
