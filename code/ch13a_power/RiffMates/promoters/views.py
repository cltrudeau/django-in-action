# RiffMates/promoters/views.py
from time import sleep

from django.shortcuts import render
from promoters.models import Promoter


def promoters(request):
    return render(request, "promoters.html")


def partial_promoters(request):
    sleep(2)
    data = {
        "promoters": Promoter.objects.all(),
    }
    return render(request, "partials/promoters.html", data)
