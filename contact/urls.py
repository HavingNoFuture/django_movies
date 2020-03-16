from django.urls import path
from contact import views

urlpatterns = [
    path('', views.ContactView.as_view(), name="contact"),
]
