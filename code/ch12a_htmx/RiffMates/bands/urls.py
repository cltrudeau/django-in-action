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
    path("add_musician/", views.edit_musician, name="add_musician"),
    path(
        "edit_musician/<int:musician_id>/",
        views.edit_musician,
        name="edit_musician",
    ),
    path("search_musicians/", views.search_musicians, name="search_musicians"),
    path("room_editor/<int:venue_id>/", views.room_editor, name="room_editor"),
    path(
        "edit_room_form/<int:room_id>/",
        views.edit_room_form,
        name="edit_room_form",
    ),
    path(
        "show_room_partial/<int:room_id>/",
        views.show_room_partial,
        name="show_room_partial",
    ),
]
