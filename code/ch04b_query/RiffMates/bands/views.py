# RiffMates/bands/views.py
from bands.models import Musician
from django.shortcuts import get_object_or_404, render


def musician(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)

    data = {
        "musician": musician,
    }

    return render(request, "musician.html", data)


def musicians(request):
    data = {
        "musicians": Musician.objects.all().order_by("last_name"),
    }

    return render(request, "musicians.html", data)
