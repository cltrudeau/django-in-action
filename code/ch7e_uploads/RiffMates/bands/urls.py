# RiffMates/bands/urls.py
from bands import views
from django.urls import path

urlpatterns = [
    path("musician/<int:musician_id>/", views.musician, name="musician"),
    path("musicians/", views.musicians, name="musicians"),
    path("band/<int:band_id>/", views.band, name="band"),
    path("bands/", views.bands, name="bands"),
    path("venues/", views.venues, name="venues"),
    path("restricted_page/", views.restricted_page, name="restricted_page"),
    path(
        "musician_restricted/<int:musician_id>/",
        views.musician_restricted,
        name="musician_restricted",
    ),
    path(
        "venues_restricted/", views.venues_restricted, name="venues_restricted"
    ),
    path("add_venue/", views.edit_venue, name="add_venue"),
    path("edit_venue/<int:venue_id>/", views.edit_venue, name="edit_venue"),
]
