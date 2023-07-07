# RiffMates/bands/urls.py
from bands import views
from django.urls import path

urlpatterns = [
    path("musician/<int:musician_id>/", views.musician, name="musician"),
]
