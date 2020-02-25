from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from movie_catalog.models import Movie, Person, Genre, Rating
from movie_catalog.forms import ReviewForm, RatingForm


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        current_user_rating = self.object.rating_set.get(ip=get_client_ip(self.request))
        context['rating_form'] = RatingForm()
        context['average_rating'] = "{0:.2f}".format(current_user_rating.get_average_rating())
        context['current_user_rating'] = current_user_rating.star.value
        return context


class AddRatingStar(View):
    """Отправка формы звезды рейтингаю"""

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip = get_client_ip(request),
                movie_id = int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)



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
