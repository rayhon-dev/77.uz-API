from django.urls import path

from . import views

urlpatterns = [
    path("ads/", views.AdCreateView.as_view(), name="create-ads"),
    path("ads/<slug:slug>/", views.AdDetailView.as_view(), name="detail-ad"),
    path(
        "categories-with-childs/",
        views.CategoriesWithChildrenView.as_view(),
        name="categories-with-childs",
    ),
    path("category/", views.CategoryListView.as_view(), name="category-list"),
]
