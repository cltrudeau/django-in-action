# RiffMates/bands/views.py
from datetime import date

from bands.forms import MusicianForm, VenueForm
from bands.models import Band, Musician, Venue
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render


def musician(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)
    musician.controller = False
    if request.user.is_staff:
        musician.controller = True
    elif hasattr(request.user, "userprofile"):
        # This view can be used by people who aren't logged in,
        # those users don't have a profile, need to validate
        # one exists before using it
        profile = request.user.userprofile
        musician.controller = profile.musician_profiles.filter(
            id=musician_id
        ).exists()

    data = {
        "musician": musician,
    }

    return render(request, "musician.html", data)


def edit_musician(request, musician_id=0):
    if musician_id != 0:
        musician = get_object_or_404(Musician, id=musician_id)
        if (
            not request.user.is_staff
            and not request.user.userprofile.musician_profiles.filter(
                id=musician_id
            ).exists()
        ):
            raise Http404("Can only edit controlled musicians")

    if request.method == "GET":
        if musician_id == 0:
            form = MusicianForm()
        else:
            form = MusicianForm(instance=musician)

    else:  # POST
        if musician_id == 0:
            musician = Musician.objects.create(birth=date(1900, 1, 1))

        form = MusicianForm(request.POST, request.FILES, instance=musician)

        if form.is_valid():
            musician = form.save()

            # Add the musician to the user's profile if this isn't staff
            if not request.user.is_staff:
                request.user.userprofile.musician_profiles.add(musician)

            return redirect("musicians")

    # Was a GET, or Form was not valid
    data = {
        "form": form,
    }

    return render(request, "edit_musician.html", data)


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
    profile = getattr(request.user, "userprofile", None)
    if profile:
        for venue in all_venues:
            # Mark the venue as "controlled" if the logged in user is
            # associated with the venue
            venue.controlled = profile.venues_controlled.filter(
                id=venue.id
            ).exists()
    else:
        # Anonymous user, can't be associated with the venue
        for venue in all_venues:
            venue.controlled = False

    items_per_page = _get_items_per_page(request)
    paginator = Paginator(all_venues, items_per_page)

    page_num = _get_page_num(request, paginator)

    page = paginator.page(page_num)

    data = {
        "venues": page.object_list,
        "page": page,
    }

    return render(request, "venues.html", data)


@login_required
def restricted_page(request):
    data = {
        "title": "Restricted Page",
        "content": "<h1>You are logged in</h1>",
    }

    return render(request, "general.html", data)


@login_required
def musician_restricted(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)
    profile = request.user.userprofile
    allowed = False

    if profile.musician_profiles.filter(id=musician_id).exists():
        allowed = True
    else:
        # User is not this musician, check if they're a band-mate
        musician_profiles = set(profile.musician_profiles.all())
        for band in musician.band_set.all():
            band_musicians = set(band.musicians.all())
            if musician_profiles.intersection(band_musicians):
                allowed = True
                break

    if not allowed:
        raise Http404("Permission denied")

    content = f"""
        <h1>Musician Page: {musician.last_name}</h1>
    """
    data = {
        "title": "Musician Restricted",
        "content": content,
    }

    return render(request, "general.html", data)


def has_venue(user):
    try:
        return user.userprofile.venues_controlled.count() > 0
    except AttributeError:
        return False


@user_passes_test(has_venue)
def venues_restricted(request):
    return venues(request)


@login_required
def edit_venue(request, venue_id=0):
    if venue_id != 0:
        venue = get_object_or_404(Venue, id=venue_id)
        if not request.user.userprofile.venues_controlled.filter(
            id=venue_id
        ).exists():
            raise Http404("Can only edit controlled venues")

    if request.method == "GET":
        if venue_id == 0:
            form = VenueForm()
        else:
            form = VenueForm(instance=venue)

    else:  # POST
        if venue_id == 0:
            venue = Venue.objects.create()

        form = VenueForm(request.POST, request.FILES, instance=venue)

        if form.is_valid():
            venue = form.save()

            # Add the venue to the user's profile
            request.user.userprofile.venues_controlled.add(venue)
            return redirect("venues")

    # Was a GET, or Form was not valid
    data = {
        "form": form,
    }

    return render(request, "edit_venue.html", data)
