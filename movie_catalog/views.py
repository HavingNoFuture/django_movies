from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from movie_catalog.models import Movie
from movie_catalog.forms import ReviewForm


class MovieListView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = "movie_catalog/movie_list.html"


class MovieDetailView(DetailView):
    """Описание фильма"""
    model = Movie
    slug_field = "slug"


class AddReview(View):
    """Отправка формы отзыва."""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(pk=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.movie_id = pk
            parent = int(request.POST.get("parent", None))
            if parent:
                form.parent_id = parent
            form.save()
        print(request.POST)
        return redirect(movie.get_absolute_url())


