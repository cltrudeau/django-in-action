# RiffMates/RiffMates/urls.py
from django.contrib import admin
from django.urls import path
from home import views as home_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("credits/", home_views.credits),
]
