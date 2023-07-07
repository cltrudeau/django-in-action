# RiffMates/bands/admin.py
from bands.models import Musician
from django.contrib import admin


@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_name",
        "first_name",
        "show_weekday",
    )
    search_fields = (
        "last_name",
        "first_name",
    )

    def show_weekday(self, obj):
        # Fetch weekday of artist's birth
        return obj.birth.strftime("%A")

    show_weekday.short_description = "Birth Weekday"
