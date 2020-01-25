from django import template
from movie_catalog.models import Category, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    """Получить список всех категорий. Использую в шапке"""
    return Category.objects.all()


@register.inclusion_tag("movie_catalog/tags/last_movies.html")
def get_last_movies(count=5):
    """Получить 5 последних фильмов, отсортированых по дате по убыванию."""
    movies = Movie.objects.order_by("-id")[:count]
    print("movies", movies)
    return {'last_movies': movies}
