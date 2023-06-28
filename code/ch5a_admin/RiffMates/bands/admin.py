# RiffMates/bands/admin.py
from django.contrib import admin

from bands.models import Musician


@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    pass
