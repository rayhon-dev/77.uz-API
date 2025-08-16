from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class PageListPagination(CustomPagination):
    page_size = 10


class AdListPagination(CustomPagination):
    page_size = 10
