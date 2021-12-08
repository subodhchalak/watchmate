from django.http import JsonResponse
from django.http.response import Http404, HttpResponse

from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from rest_framework.parsers import JSONParser
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.throttling import (AnonRateThrottle, ScopedRateThrottle,
                                       UserRateThrottle)
from rest_framework.views import APIView

from watchlist_app.api.pagination import (WatchlistCursorPagination,
                                          WatchlistPagination,
                                          WatclistLimitOffsetPagination)
from watchlist_app.api.permissions import (IsAdminOrReadOnly,
                                           IsReviewUserOrReadOnly)
from watchlist_app.api.serializers import (ReviewSerializer,
                                           StreamPlatformSerializer,
                                           WatchListSerializer)

from watchlist_app.api.throttling import ReviewCreateThrottle
from watchlist_app.models import Review, StreamPlatform, WatchList

# Create your views here.



# ---------------------------------------------------------------------------- #
#                               Review Model View                              #
# ---------------------------------------------------------------------------- #
class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)
    
    
    
class ReviewCreateView(generics.CreateAPIView):
    # queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    throttle_classes=[ReviewCreateThrottle]
    
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):       # Called by CreateModelMixin when saving a new object instance.
        pk=self.kwargs['pk']                    # Accessing 'pk' from 'kwargs' dictionary
        watchlist=WatchList.objects.get(pk=pk)       # getting single show through its primary key 'pk'
        
        review_user=self.request.user                  # get the logged in current user
        
        review_queryset=Review.objects.filter(watchlist=watchlist, review_user=review_user)   # passing values to related names metioned in models
        # filtering review list on current show and current user
        
        if review_queryset.exists():        # if current user is already exists, means he/she has already posted a review
            raise ValidationError("You have already posted review for this show!")
        
        if watchlist.number_rating==0:
            watchlist.avg_rating=serializer.validated_data['rating']             # old rating = new rating
        else:
            
            watchlist.avg_rating=(watchlist.avg_rating + serializer.validated_data['rating'])/2          # Calulation is not correct
            
        watchlist.number_rating = watchlist.number_rating + 1                  # increase number_rating counter by one
    
        watchlist.save()                                                  # save show with updated rating info
        
        serializer.save(watchlist=watchlist, review_user=review_user)         # 'watchlist' is ForeignKey attribute mentioned in model 'Review'
        # 'review_user' is ForeignKey attribute mentioned in model 'Review'


class ReviewListView(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class =ReviewSerializer
    
    # throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'reviews'
    
    # permission_classes = [IsAuthenticated]
    
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['review_user__username', 'active']
    
    filter_beckends=[filters.OrderingFilter]
    ordering_fields = ['rating']
    ordering = ['rating']
    
    
    def get_queryset(self):                          # overridding existing method
        pk=self.kwargs['pk']                         # Accessing 'pk' from 'kwargs' dictionary
        show=Review.objects.filter(watchlist=pk)     # 'watchlist' is ForeignKey attribute mentioned in model 'Review'
        return show   
    
    
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    # throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'reviewDetail'
    
    
    
# ---------------------------------------------------------------------------- #
#                             WatchList Model Views                            #
# ---------------------------------------------------------------------------- #

class WatchListView(generics.ListCreateAPIView):
    queryset=WatchList.objects.all()
    serializer_class=WatchListSerializer
    permission_classes=[IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    
    # filter_backends =[filters.SearchFilter, DjangoFilterBackend]
    # filterset_fields = ['title', 'streamPlatform__name', 'active']
    # search_fields=['title', 'active']
    # filter_beckends=[filters.OrderingFilter]
    # ordering_fields = ['avg_rating']
    # ordering=['ordering']
    
    pagination_class = WatchlistCursorPagination
    
    
    
class WatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=WatchList.objects.all()
    serializer_class=WatchListSerializer
    permission_classes = [IsAdminOrReadOnly]
        
        
    
    
# ---------------------------------------------------------------------------- #
#                          StreamPlatform ModelViewSet                         #
# ---------------------------------------------------------------------------- #

class StreamPlatformView(viewsets.ModelViewSet):
    queryset=StreamPlatform.objects.all()
    serializer_class=StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    
# class StreamPlatformDetailView(viewsets.ModelViewSet):
#     queryset=StreamPlatform.objects.all()
#     serializer_class=StreamPlatformSerializer
#     permission_classes = [IsAdminOrReadOnly]
        
        
# ---------------------------------------------------------------------------- #
#                          StreamPlatform ViewSet                              #
# ---------------------------------------------------------------------------- #


# class StreamPlatformView(viewsets.ViewSet):
    
#     def list(self, request):
#         queryset=StreamPlatform.objects.all()
#         serializer=StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk):
#         queryset=StreamPlatform.objects.all()
#         platform=get_object_or_404(queryset, pk=pk)
#         serializer=StreamPlatformSerializer(platform)
#         return Response(serializer.data)
        
        
#     def create(self, request):
#         serializer=StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
    
#     def destroy(self, request, pk):
#         queryset=StreamPlatform.objects.get(pk=pk)
#         queryset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
        
# ------------------------------------- X ------------------------------------ #
    


# class StreamPlatformView(generics.ListCreateAPIView):
#     queryset=StreamPlatform.objects.all()
#     serializer_class=StreamPlatformSerializer
    
# class StreamPlatformDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset=StreamPlatform.objects.all()
#     serializer_class=StreamPlatformSerializer
    




# ---------------------------------------------------------------------------- #
#                                APIView Classes                               #
# ---------------------------------------------------------------------------- #

# class StreamPlaformAV(APIView):
    
#     def get(selfm, request, format=None):
#         platforms = StreamPlatform.objects.all()
#         serializer= StreamPlatformSerializer(platforms, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request, format=None):
#         serializer=StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
# class StreamPlatformDetailAV(APIView):
    
#     def get_object(self, request, pk, format=None):
#         try:
#             return StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             raise Http404
        
        
#     def get(self, request, pk, format=None):
#         platform=StreamPlatform.objects.get(pk=pk)
#         serializer=StreamPlatformSerializer(platform)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk, format=None):
#         platform=StreamPlatform.objects.get(pk=pk)
#         serializer=StreamPlatformSerializer(platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk, format=None):
#         platform=StreamPlatform.objects.get(pk=pk)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        



# class WatchListAV(APIView):
    
#     def get(self, request, format=None):
#         show_list=WatchList.objects.all()
#         serializer=WatchListSerializer(show_list, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer=WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
   
   
   
        
        
# class WatchDetailAV(APIView):
    
#     def get_object(self, request, pk, format=None):
#         try:
#             show=WatchList.objects.get(pk=pk)
#             return show
#         except WatchList.DoesNotExist:
#             data={"Error":"Show does not exist!"}
#             return JsonResponse(data)
        
#     def get(self, request, pk, format=None):
#         show= WatchList.objects.get(pk=pk)
#         serializer=WatchListSerializer(show)
#         return Response(serializer.data, status=status.HTTP_200_OK)
        
#     def put(self, request, pk, format=None):
#         show= WatchList.objects.get(pk=pk)
#         serializer=WatchListSerializer(show, request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk, format=None):
#         show= WatchList.objects.get(pk=pk)
#         show.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)















# class ReviewsAV(APIView):
    
#     def get(self, request, format=None):
#         reviews=Review.objects.all()
#         serializer=ReviewSerializer(reviews, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
        
#     def post(self, request, format=None):
#         serializer=ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# class ReviewsDetailAV(APIView):
    
#     def get_object(self, request, pk, format=None):
#         try:
#             return Review.objects.get(pk=pk)
#         except Review.DoesNotExist:
#             raise Http404
        
#     def get(self, request, pk, format=None):
#         review=Review.objects.get(pk=pk)
#         serializer=ReviewSerializer(review)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk, format=None):
#         review=Review.objects.get(pk=pk)
#         serializer=ReviewSerializer(review, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk, format=None):
#         review=Review.objects.get(pk=pk)
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        



# @api_view(['GET', 'POST'])
# def movieList(request):
#     if request.method == 'GET':
#         movies=Movie.objects.all()
#         serializer=WatchListSerializer(movies, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     if request.method == 'POST':
#         serializer=WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
# @api_view(['GET', 'PUT', 'DELETE'])
# def movieDetail(request, pk):
#     try:
#         movie = Movie.objects.get(pk=pk)
#     except Movie.DoesNotExist:
#         return Response({"Error": "Movie Doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer=WatchListSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method=="PUT":
#         serializer=WatchListSerializer(movie, request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method=="DELETE":
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT) 
