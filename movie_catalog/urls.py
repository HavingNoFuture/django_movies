from django.urls import path
from movie_catalog import views

urlpatterns = [
    path('', views.MovieListView.as_view(), name="movie_list"),
    path('filter/', views.MovieFilterView.as_view(), name="movie_filter"),
    path('filter-json/', views.JsonMovieFilterView.as_view(), name="movie_filter_json"),
    path('persons/<str:slug>', views.PersonDetailView.as_view(), name="person_detail"),
    path('add_review/<int:pk>', views.AddReview.as_view(), name="add_review"),
    path('<str:slug>', views.MovieDetailView.as_view(), name="movie_detail"),
]
