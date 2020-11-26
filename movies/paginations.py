from rest_framework import pagination


class TenPageNumberPagination(pagination.PageNumberPagination):
    """
    Custom page number pagination.
    It allows 10 elements per page.
    """
    page_size = 10
