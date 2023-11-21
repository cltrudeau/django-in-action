# RiffMates/bands/api.py
from typing import Optional

from api_auth import api_key
from bands.models import Band, Musician, Room, Venue
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.text import slugify
from ninja import Field, FilterSchema, ModelSchema, Query, Router

router = Router()

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class RoomSchema(ModelSchema):
    class Config:
        model = Room
        model_fields = ["id", "name"]


class VenueOut(ModelSchema):
    slug: str
    url: str
    rooms: list[RoomSchema] = Field(..., alias="room_set")

    class Config:
        model = Venue
        model_fields = ["id", "name", "description"]

    @staticmethod
    def resolve_slug(obj):
        slug = slugify(obj.name) + "-" + str(obj.id)
        return slug

    @staticmethod
    def resolve_url(obj):
        url = reverse(
            "api-1.0:fetch_venue",
            args=[
                obj.id,
            ],
        )
        return url


class VenueIn(ModelSchema):
    class Config:
        model = Venue
        model_fields = ["name", "description"]


class VenueFilter(FilterSchema):
    name: Optional[str] = Field(q=["name__istartswith"])


class MusicianIn(ModelSchema):
    class Config:
        model = Musician
        model_fields = [
            "first_name",
            "last_name",
            "birth",
            "description",
        ]


class MusicianOut(ModelSchema):
    class Config:
        model = Musician
        model_fields = [
            "id",
            "first_name",
            "last_name",
            "birth",
            "description",
        ]


class BandSchema(ModelSchema):
    musicians: list[MusicianOut]

    class Config:
        model = Band
        model_fields = ["id", "name"]


# ---------------------------------------------------------------------------
# API Views
# ---------------------------------------------------------------------------

# @router.get("/venues/", response=list[VenueOut])
# def venues(request, name=None):
#     venues = Venue.objects.all()
#     if name is not None:
#         venues = venues.filter(name__istartswith=name)
#
#     return venues


@router.get("/venues/", response=list[VenueOut])
def venues(request, filters: VenueFilter = Query(...)):
    venues = Venue.objects.all()
    venues = filters.filter(venues)
    return venues


@router.get("/venue/{venue_id}/", response=VenueOut, url_name="fetch_venue")
def fetch_venue(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    return venue


@router.post("/venue/", response=VenueOut, auth=api_key)
def create_venue(request, payload: VenueIn):
    venue = Venue.objects.create(**payload.dict())
    return venue


@router.put("/venue/{venue_id}/", response=VenueOut, auth=api_key)
def update_venue(request, venue_id, payload: VenueIn):
    venue = get_object_or_404(Venue, id=venue_id)
    for key, value in payload.dict().items():
        setattr(venue, key, value)

    venue.save()
    return venue


@router.delete("/venue/{venue_id}/", auth=api_key)
def delete_venue(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    venue.delete()

    return {"success": True}


@router.get("/bands/", response=list[BandSchema])
def list_bands(request):
    return Band.objects.all()


@router.put("/musician/{musician_id}/", response=MusicianOut, auth=api_key)
def update_musician(request, musician_id, payload: MusicianIn):
    musician = get_object_or_404(Musician, id=musician_id)
    for key, value in payload.dict().items():
        setattr(musician, key, value)

    musician.save()
    return musician
