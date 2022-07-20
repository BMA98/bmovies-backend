from rest_framework import pagination


class TenPageNumberPagination(pagination.PageNumberPagination):
    """
    Custom page number pagination.
    It allows 10 elements per page.
    """
    page_size = 10
    page_size_query_param = 'page_size'

    def get_page_size(self, request):
        if self.page_size_query_param:
            page_size = request.query_params.get(self.page_size_query_param)
            if not page_size:
                return self.page_size
            elif int(page_size) > 0:
                return page_size
            else:
                return None
        return self.page_size
