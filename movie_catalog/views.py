from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Movie


class MovieListView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = "movie_catalog/movie_list.html"


class MovieDetailView(DetailView):
    """Описание фильма"""
    model = Movie
    slug_field = "slug"


