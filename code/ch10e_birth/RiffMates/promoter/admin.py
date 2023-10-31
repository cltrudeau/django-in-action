# RiffMates/promoter/admin.py
from django.contrib import admin
from promoter.models import Promoter


@admin.register(Promoter)
class PromoterAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "common_name", "famous_for")
