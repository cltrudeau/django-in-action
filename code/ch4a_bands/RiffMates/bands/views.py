# RiffMates/bands/views.py


def musician(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)
