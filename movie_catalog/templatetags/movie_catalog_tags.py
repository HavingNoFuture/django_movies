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
    movies = Movie.objects.only("slug", "title", "poster").filter(draft=False).order_by("-id")[:count]
    return {'last_movies': movies}
