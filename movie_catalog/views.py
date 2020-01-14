from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from .models import Movie


class MovieListView(View):
    """Список фильмов"""
    def get(self, request):
        movies = Movie.objects.all()
        return render(request, "movie_catalog/movie_list.html", {"movie_list": movies})


class MovieDetailView(View):
    """Описание фильма"""
    def get(self, request, slug):
        movie = get_object_or_404(Movie, slug=slug)
        return render(request, "movie_catalog/movie_detail.html", {"movie": movie})

