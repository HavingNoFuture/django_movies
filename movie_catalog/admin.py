from django.contrib import admin

from movie_catalog.models import Person, Genre, Category, Movie, MovieShots, RatingStars, Rating, Reviews


admin.site.register(Category)
admin.site.register(Person)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieShots)
admin.site.register(RatingStars)
admin.site.register(Rating)
admin.site.register(Reviews)
