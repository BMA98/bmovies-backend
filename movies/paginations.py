from rest_framework import pagination


class TenPageNumberPagination(pagination.PageNumberPagination):
    """Custom page number pagination."""

    page_size = 10
