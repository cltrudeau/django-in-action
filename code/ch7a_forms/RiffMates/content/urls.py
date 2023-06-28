# RiffMates/content/urls.py
from django.urls import path

from content import views

urlpatterns = [
    path("comment/", views.comment, name="comment"),
    path("comment_accepted/", views.comment_accepted, name="comment_accepted"),
]
