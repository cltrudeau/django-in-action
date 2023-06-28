# RiffMates/bands/forms.py
from django import forms
from bands.models import Venue, Musician

VenueForm = forms.modelform_factory(
    Venue, fields=["name", "description", "picture"]
)

MusicianForm = forms.modelform_factory(
    Musician,
    fields=["first_name", "last_name", "birth", "description", "picture"],
)
