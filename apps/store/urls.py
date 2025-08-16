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
    path(
        "favourite-product-create-by-id/",
        views.FavouriteProductCreateByIDView.as_view(),
        name="favourite-create-by-id",
    ),
    path(
        "favourite-product-by-id/<int:pk>/delete/",
        views.FavouriteProductDeleteByIDView.as_view(),
        name="favourite-delete-by-id",
    ),
    path(
        "favourite-product-create/",
        views.FavouriteProductCreateView.as_view(),
        name="favourite-create",
    ),
    path(
        "favourite-product/<int:pk>/delete/",
        views.FavouriteProductDeleteView.as_view(),
        name="favourite-delete",
    ),
    path("list/ads/", views.AdListView.as_view(), name="list-ads"),
]
