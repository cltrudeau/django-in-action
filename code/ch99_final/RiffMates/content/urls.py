# RiffMates/content/urls.py
from content import views
from django.urls import path

urlpatterns = [
    path("comment/", views.comment, name="comment"),
    path("comment_accepted/", views.comment_accepted, name="comment_accepted"),
    path("list_ads/", views.list_ads, name="list_ads"),
    path("seeking_ad/", views.seeking_ad, name="seeking_ad"),
    path(
        "edit_seeking_ad/<int:ad_id>/", views.seeking_ad, name="edit_seeking_ad"
    ),
    path("search_ads/", views.search_ads, name="search_ads"),
]
