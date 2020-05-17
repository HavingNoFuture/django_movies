from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from movie_catalog.models import Movie, Person, Genre, Rating, get_client_ip
from movie_catalog.forms import ReviewForm, RatingForm


class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_year_list(self):
        """Отдает список годов фильмов в порядке убывания"""
        return Movie.objects.filter(draft=False).values_list("year", flat=True).distinct().order_by("-year")

    def get_genre_list(self):
        """Отдает список жанров фильмов"""
        return Genre.objects.all().only("name").distinct().order_by("name")


class MovieListView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.only("id", "title", "tagline", "slug", "poster").filter(draft=False)
    paginate_by = 3


class MovieDetailView(GenreYear, DetailView):
    """Описание фильма"""
    model = Movie
    queryset = Movie.objects.select_related().filter(draft=False)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            current_user_rating = self.object.get_current_user_rating(self.request)
            context['current_user_rating'] = current_user_rating.star.value
            context['average_rating'] = self.object.get_avg_rating_str()
        except Rating.DoesNotExist:
            context['current_user_rating'] = 0
            context['average_rating'] = "0.00"
        context['rating_form'] = RatingForm()
        context['review_form'] = ReviewForm()
        return context


class AddRatingStar(View):
    """Отправка формы звезды рейтингаю"""

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
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
            try:
                parent = int(request.POST.get("parent", None))
                form.parent_id = parent
            except ValueError:
                pass
            form.save()
        return redirect(movie.get_absolute_url())


class PersonDetailView(DetailView):
    """Описание актера или режиссера"""
    model = Person


class MovieFilterView(GenreYear, ListView):
    """Фильтр для фильмов по году и жанру"""
    paginate_by = 3

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre")) &
            Q(draft=False)
        ).distinct().only("id", "title", "tagline", "slug", "poster").order_by("-id")
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class JsonMovieFilterView(ListView):
    """Фильтр для фильмов по году и жанру в json"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "slug", "poster").filter(draft=False)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)


class MovieSearchView(GenreYear, ListView):
    """Поиск фильма"""
    paginate_by = 3

    def get_queryset(self):
        queryset = Movie.objects.filter(title__icontains=self.request.GET.get("q"))\
            .only("id", "title", "tagline", "slug", "poster").order_by("-id").filter(draft=False)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
