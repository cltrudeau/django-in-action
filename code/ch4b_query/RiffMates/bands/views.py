# RiffMates/bands/views.py
from django.shortcuts import get_object_or_404, render


def musician(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)


def musicians(request):
    data = {
        "musicians": Musician.objects.all().order_by("last_name"),
    }

    return render(request, "musicians.html", data)
