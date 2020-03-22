from modeltranslation.translator import register, TranslationOptions
from .models import Category, Person, Movie, Genre, MovieShots, Country


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Person)
class PersonTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'description')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description')


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(MovieShots)
class MovieShotsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
