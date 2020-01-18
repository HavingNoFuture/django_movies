from django.contrib import admin

from movie_catalog.models import Person, Genre, Category, Movie, MovieShots, RatingStars, Rating, Reviews


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name", "id")


class ReviewsInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "year", "draft")
    list_display_links = ("title", "id")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name", "year")
    inlines = [ReviewsInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    fieldsets = (
        (None, {
           "fields": (("title", "tagline"), )
        }),
        (None, {
            "fields": (("genres", "category"),)
        }),
        (None, {
            "fields": ("description", "poster")
        }),
        (None, {
            "fields": (("year", "world_premier", "country"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        ("Persons", {
            "classes": ("collapse", ),
            "fields": (("actors", "directors",),)
        }),
        ("Options", {
            "fields": (("slug", "draft"),)
        }),
    )


@admin.register(Reviews)
class RewievsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "parent", "movie")
    list_display_links = ("name", "email", "id")
    list_filter = ("movie", "email", "parent")
    search_fields = ("name", "email", "movie")
    readonly_fields = ("name", "email")



@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "second_name", "age")
    list_display_links = ("last_name", "first_name", "id")
    list_filter = ("age", )
    search_fields = ("first_name", "last_name", "second_name")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name", "id")
    search_fields = ("name", )


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "movie", )
    list_display_links = ("title", "id")
    list_filter = ("movie__title", )
    search_fields = ("title", "movie")


@admin.register(RatingStars)
class RatingStarsAdmin(admin.ModelAdmin):
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "ip", "movie", "star")
    list_display_links = ("ip", "id")
    list_filter = ("movie", "ip", "star")
    search_fields = ("ip", "email")
    readonly_fields = ("ip", "movie", "star")
