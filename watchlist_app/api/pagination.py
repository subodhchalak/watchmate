from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination



class WatchlistPagination(PageNumberPagination):
    page_size=5
    page_query_param="p"  # A string value indicating the name of the query parameter to use for the pagination control.
    page_size_query_param="size"                  # client can decide record size per page_size_query_param
    max_page_size=20                              # restricting client with max page size to avoid very high number imput
    
    
class WatclistLimitOffsetPagination(LimitOffsetPagination):
    default_limit=5
    max_limit=20
    
    
class WatchlistCursorPagination(CursorPagination):
    page_size=5
    ordering = 'created'              # default= '-created'
    curser_query_params = {}
    