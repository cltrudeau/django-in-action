# RiffMates/promoters/urls.py
from django.urls import path
from promoters import views

urlpatterns = [
    path("promoters/", views.promoters, name="promoters"),
    path(
        "partial_promoters/", views.partial_promoters, name="partial_promoters"
    ),
]
