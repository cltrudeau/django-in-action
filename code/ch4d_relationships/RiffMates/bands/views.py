# RiffMates/bands/views.py
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from bands.models import Musician


def musician(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)


def musicians(request):
    all_musicians = Musician.objects.all().order_by("last_name")
    paginator = Paginator(all_musicians, 2)
    page_num = request.GET.get("page", 1)
    page_num = int(page_num)

    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages

    page = paginator.page(page_num)

    data = {
        "musicians": page.object_list,
        "page": page,
    }

    return render(request, "musicians.html", data)
