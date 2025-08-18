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
    path("my-ads/", views.MyAdsListAPIView.as_view(), name="my-ads-list"),
    path("my-ads/<int:pk>/", views.MyAdDetailUpdateDeleteView.as_view(), name="my-ads-detail"),
    path(
        "my-favourite-product-by-id/",
        views.MyFavouriteProductByIdView.as_view(),
        name="my-favourite-product-by-id",
    ),
    path(
        "my-favourite-product/", views.MyFavouriteProductView.as_view(), name="my-favourite-product"
    ),
    path("my-search/", views.MySearchCreateView.as_view(), name="my-search-create"),
    path("my-search/list/", views.MySearchListView.as_view(), name="my-search-list"),
    path("my-search/<int:pk>/delete/", views.MySearchDeleteView.as_view(), name="my-search-delete"),
    path(
        "product-download/<slug:slug>/",
        views.ProductDownloadView.as_view(),
        name="product-download",
    ),
    path(
        "product-image-create/", views.ProductImageCreateView.as_view(), name="product-image-create"
    ),
    path(
        "search/category-product/",
        views.CategoryProductSearchView.as_view(),
        name="category-product-search",
    ),
    path("search/complete/", views.SearchCompleteView.as_view(), name="search-complete"),
    path(
        "search/count-increase/<int:product_id>/",
        views.SearchCountIncreaseView.as_view(),
        name="search-count",
    ),
    path("search/populars/", views.PopularsView.as_view(), name="popular-searches"),
    path("search/sub-category/", views.SubCategoryListView.as_view(), name="sub-category-list"),
]
