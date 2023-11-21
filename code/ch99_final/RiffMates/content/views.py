# RiffMates/content/views.py
import urllib
from time import sleep

from bands.views import _get_items_per_page, _get_page_num
from content.forms import CommentForm, SeekingAdForm
from content.models import MusicianBandChoice, SeekingAd
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render


def comment(request):
    if request.method == "GET":
        form = CommentForm()

    else:  # POST
        form = CommentForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            comment = form.cleaned_data["comment"]

            message = f"""\
                Received comment from {name}\n\n
                {comment}
            """

            send_mail(
                "Received comment",
                message,
                "admin@example.com",
                ["admin@example.com"],
                fail_silently=False,
            )
            return redirect("comment_accepted")

    # Was a GET, or Form was not valid
    data = {
        "form": form,
    }

    return render(request, "comment.html", data)


def comment_accepted(request):
    data = {
        "content": """
            <h1> Comment Accepted </h1>

            <p> Thanks for submitting a comment to <i>RiffMates</i> </p>
        """
    }

    return render(request, "general.html", data)


def list_ads(request):
    data = {
        "seeking_musician": SeekingAd.objects.filter(
            seeking=MusicianBandChoice.MUSICIAN
        ),
        "seeking_band": SeekingAd.objects.filter(
            seeking=MusicianBandChoice.BAND
        ),
    }

    return render(request, "list_ads.html", data)


@login_required
def seeking_ad(request, ad_id=0):
    if request.method == "GET":
        if ad_id == 0:
            form = SeekingAdForm()
        elif request.user.is_staff:
            ad = get_object_or_404(SeekingAd, id=ad_id)
            form = SeekingAdForm(instance=ad)
        else:
            ad = get_object_or_404(SeekingAd, id=ad_id, owner=request.user)
            form = SeekingAdForm(instance=ad)

    else:  # POST
        if ad_id == 0:
            form = SeekingAdForm(request.POST)
        elif request.user.is_staff:
            ad = get_object_or_404(SeekingAd, id=ad_id)
            form = SeekingAdForm(request.POST, instance=ad)
        else:
            ad = get_object_or_404(SeekingAd, id=ad_id, owner=request.user)
            form = SeekingAdForm(request.POST, instance=ad)

        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.save()

            return redirect("list_ads")

    # Was a GET, or Form was not valid
    data = {
        "form": form,
    }

    return render(request, "seeking_ad.html", data)


def search_ads(request):
    search_text = request.GET.get("search_text", "")
    search_text = urllib.parse.unquote(search_text)
    search_text = search_text.strip()

    ads = []

    if search_text:
        parts = search_text.split()

        q = Q(content__icontains=parts[0])
        for part in parts[1:]:
            q |= Q(content__icontains=part)

        ads = SeekingAd.objects.filter(q)

    items_per_page = _get_items_per_page(request)
    paginator = Paginator(ads, items_per_page)
    page_num = _get_page_num(request, paginator)
    page = paginator.page(page_num)

    data = {
        "search_text": search_text,
        "ads": page.object_list,
        "has_more": page.has_next(),
        "next_page": page_num + 1,
    }

    if request.htmx:
        if page_num > 1:
            sleep(2)

        return render(request, "partials/ad_results.html", data)

    return render(request, "search_ads.html", data)
