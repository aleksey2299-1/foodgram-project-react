from rest_framework.pagination import PageNumberPagination

from foodgram_backend import constants


class RecipePagination(PageNumberPagination):
    page_size = constants.DEFAULT_PAGE_LIMIT
    page_size_query_param = 'limit'
