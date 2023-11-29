from rest_framework.pagination import LimitOffsetPagination

from foodgram_backend import constants


class RecipePagination(LimitOffsetPagination):
    default_limit = constants.DEFAULT_PAGE_LIMIT
