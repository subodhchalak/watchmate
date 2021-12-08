# from django.shortcuts import render

# from watchlist_app.models import Movie

# from django.http import JsonResponse

# # Create your views here.


# def movieList(request):
#     movies=Movie.objects.all()
#     movies=list(movies.values())      # convert queryset into list iterable
#     data={'movies':movies}
#     return JsonResponse(data)


# def movieDetail(request, pk):
#     movie=Movie.objects.get(pk=pk)
#     data={
#         'name':movie.name,
#         'description':movie.description,
#         'active':movie.active,
#     }
#     return JsonResponse(data)