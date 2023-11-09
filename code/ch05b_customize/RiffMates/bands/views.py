# RiffMates/bands/views.py
from bands.models import Band, Musician, Venue
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render


def musician(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)

    data = {
        "musician": musician,
    }

    return render(request, "musician.html", data)


def _get_items_per_page(request):
    # Determine how many items to show per page, disallowing <1 or >50
    items_per_page = int(request.GET.get("items_per_page", 10))
    if items_per_page < 1:
        items_per_page = 10
    if items_per_page > 50:
        items_per_page = 50

    return items_per_page


def _get_page_num(request, paginator):
    # Get current page number for Pagination, using reasonable defaults
    page_num = int(request.GET.get("page", 1))

    if page_num < 1:
        page_num = 1
    elif page_num > paginator.num_pages:
        page_num = paginator.num_pages

    return page_num


def musicians(request):
    all_musicians = Musician.objects.all().order_by("last_name")
    items_per_page = _get_items_per_page(request)
    paginator = Paginator(all_musicians, items_per_page)
    page_num = _get_page_num(request, paginator)
    page = paginator.page(page_num)

    data = {
        "musicians": page.object_list,
        "page": page,
    }

    return render(request, "musicians.html", data)


def band(request, band_id):
    data = {
        "band": get_object_or_404(Band, id=band_id),
    }

    return render(request, "band.html", data)


def bands(request):
    all_bands = Band.objects.all().order_by("name")
    items_per_page = _get_items_per_page(request)
    paginator = Paginator(all_bands, items_per_page)

    page_num = _get_page_num(request, paginator)

    page = paginator.page(page_num)

    data = {
        "bands": page.object_list,
        "page": page,
    }

    return render(request, "bands.html", data)


def venues(request):
    all_venues = Venue.objects.all().order_by("name")
    items_per_page = _get_items_per_page(request)
    paginator = Paginator(all_venues, items_per_page)

    page_num = _get_page_num(request, paginator)

    page = paginator.page(page_num)

    data = {
        "venues": page.object_list,
        "page": page,
    }

    return render(request, "venues.html", data)
