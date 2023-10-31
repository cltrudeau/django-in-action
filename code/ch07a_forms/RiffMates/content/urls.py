# RiffMates/content/urls.py
from content import views
from django.urls import path

urlpatterns = [
    path("comment/", views.comment, name="comment"),
    path("comment_accepted/", views.comment_accepted, name="comment_accepted"),
]
