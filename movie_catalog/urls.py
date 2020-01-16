from django.urls import path
from movie_catalog import views

urlpatterns = [
    path('', views.MovieListView.as_view(), name="movie_list"),
    path('<str:slug>', views.MovieDetailView.as_view(), name="movie_detail"),
    path('add_review/<int:pk>', views.AddReview.as_view(), name="add_review"),
]
