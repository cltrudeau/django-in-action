# RiffMates/bands/forms.py
from bands.models import Venue
from django import forms

VenueForm = forms.modelform_factory(
    Venue, fields=["name", "description", "picture"]
)
