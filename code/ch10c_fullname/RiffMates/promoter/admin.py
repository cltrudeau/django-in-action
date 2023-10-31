# RiffMates/promoter/admin.py
from django.contrib import admin
from promoter.models import Promoter


@admin.register(Promoter)
class PromoterAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "common_name",
        "first_name",
        "last_name",
        "famous_for",
    )
