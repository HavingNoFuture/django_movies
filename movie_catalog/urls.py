from django.urls import path
from movie_catalog import views

urlpatterns = [
    path('catalog/', views.MovieListView.as_view(), name="movie_list"),
    path('<str:slug>', views.MovieDetailView.as_view(), name="movie_detail"),
]
