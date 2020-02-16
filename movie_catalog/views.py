from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from movie_catalog.models import Movie, Person, Genre
from movie_catalog.forms import ReviewForm


class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_year_list(self):
        """Отдает список годов фильмов в порядке убывания"""
        return Movie.objects.filter(draft=False).values_list("year", flat=True).distinct().order_by("-year")

    def get_genre_list(self):
        """Отдает список жанров фильмов"""
        return Genre.objects.all().distinct().order_by("name")


class MovieListView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(GenreYear, DetailView):
    """Описание фильма"""
    model = Movie


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


class PersonDetailView(DetailView):
    """Описание актера или режиссера"""
    model = Person


class MovieFilterView(GenreYear, ListView):
    """Фильтр для фильмов по году и жанру"""

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        )
        return queryset


class JsonMovieFilterView(ListView):
    """Фильтр для фильмов по году и жанру в json"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "slug", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)
