# RiffMates/content/urls.py
from django.urls import path

from content import views

urlpatterns = [
    path("comment/", views.comment, name="comment"),
    path("comment_accepted/", views.comment_accepted, name="comment_accepted"),
    path("list_ads/", views.list_ads, name="list_ads"),
    path("seeking_ad/", views.seeking_ad, name="seeking_ad"),
    path(
        "edit_seeking_ad/<int:ad_id>/", views.seeking_ad, name="edit_seeking_ad"
    ),
]
