# RiffMates/home/views.py
from django.http import HttpResponse


def credits(request):
    content = "Nicky\nYour Name"

    return HttpResponse(content, content_type="text/plain")
