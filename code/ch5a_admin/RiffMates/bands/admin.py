# RiffMates/bands/admin.py
from bands.models import Musician
from django.contrib import admin


@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    pass
