# RiffMates/home/views.py
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render


def credits(request):
    content = "Nicky\nYour Name"

    return HttpResponse(content, content_type="text/plain")


def about(request):
    content = [
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        "  <title>RiffMates About</title>",
        "</head>",
        "<body>",
        "  <h1>RiffMates About</h1>",
        "  <p>",
        "    RiffMates is a for musicians seeking musicians. Find your next ",
        "    band or band-mate. Find your next gig.",
        "  </p>",
        "</body>",
        "</html>",
    ]

    content = "\n".join(content)
    return HttpResponse(content)


def version(request):
    data = {
        "version": "0.0.1",
    }

    return JsonResponse(data)


def news(request):
    data = {
        "news": [
            "RiffMates now has a news page!",
            "RiffMates has its first web page",
        ],
    }

    return render(request, "news.html", data)
