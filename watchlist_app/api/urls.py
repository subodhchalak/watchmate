from django.urls import path, include
from rest_framework.routers import DefaultRouter


from watchlist_app.api.views import *




router=DefaultRouter()
router.register('stream', StreamPlatformView, basename='streamplatform')
# router.register('stream', StreamPlatformDetailView, basename='streamplatform_detail')



urlpatterns = [
      
    path('list/', WatchListView.as_view(), name='showList'),
    path('list/<int:pk>/', WatchDetailView.as_view(), name='showDetail'),
    
    path('', include(router.urls)),
    
    path('list/<int:pk>/reviews/', ReviewListView.as_view(), name='reviews'),
    path('list/<int:pk>/reviewCreate/', ReviewCreateView.as_view(), name='reviewCreate'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='reviewDetail'),
    
    path('userreviews/', UserReview.as_view(), name='userreviews')
    
]



# urlpatterns = [
#     # path('list/', movieList, name='movieList'),
#     # path('list/<int:pk>/', movieDetail, name='movieDetail'),
    
#     # path('platforms/', StreamPlatformView.as_view(), name='platforms'),
#     # path('platforms/<int:pk>/', StreamPlatformDetailView.as_view(), name='platformDetail'),
    
#     # path('reviews/', ReviewsAV.as_view(), name='reviews'),
#     # path('reviews/<int:pk>', ReviewsDetailAV.as_view(), name='reviewDetail'),
    
# ]