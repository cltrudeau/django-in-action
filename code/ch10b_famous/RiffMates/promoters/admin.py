# RiffMates/promoters/admin.py
from django.contrib import admin
from promoters.models import Promoter


@admin.register(Promoter)
class PromoterAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "famous_for")
