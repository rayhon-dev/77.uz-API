from django.urls import path
from . import views


urlpatterns = [
    path('ads/', views.AdCreateView.as_view(), name='create-ads'),
    path('ads/<slug:slug>/', views.AdDetailView.as_view(), name='detail-ad'),
]