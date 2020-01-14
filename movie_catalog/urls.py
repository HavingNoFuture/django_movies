from django.urls import path
from movie_catalog import views

urlpatterns = [
    path('catalog/', views.MovieView.as_view(), name="movie_catalog"),
]
