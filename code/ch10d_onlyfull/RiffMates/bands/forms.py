# RiffMates/bands/forms.py
from bands.models import Musician, Venue
from django import forms

VenueForm = forms.modelform_factory(
    Venue, fields=["name", "description", "picture"]
)

MusicianForm = forms.modelform_factory(
    Musician,
    fields=["first_name", "last_name", "birth", "description", "picture"],
)
