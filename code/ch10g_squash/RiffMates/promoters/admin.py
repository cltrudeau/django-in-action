# RiffMates/promoters/admin.py
from django.contrib import admin
from promoters.models import Promoter


@admin.register(Promoter)
class PromoterAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "common_name", "famous_for")
