# RiffMates/content/models.py
from bands.models import Band, Musician
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class SeekingChoice(models.TextChoices):
    MUSICIAN = "M"
    BAND = "B"


class SeekingAd(models.Model):
    date = models.DateField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    seeking = models.CharField(max_length=1, choices=SeekingChoice.choices)
    musician = models.ForeignKey(
        Musician, on_delete=models.SET_NULL, blank=True, null=True
    )
    band = models.ForeignKey(
        Band, on_delete=models.SET_NULL, blank=True, null=True
    )
    content = models.TextField()

    class Meta:
        ordering = [
            "date",
        ]

    def __str__(self):
        return f"SeekingAd(id={self.id}, seeking={self.seeking})"

    def clean(self):
        if self.seeking == SeekingChoice.MUSICIAN:
            if self.band is None:
                raise ValidationError(
                    "Band field required when seeking a musician"
                )
            if self.musician is not None:
                raise ValidationError(
                    (
                        "Musician field should be empty for a band "
                        "seeking a musician"
                    )
                )

        else:  # self.seeking == SeekingChoice.Band
            if self.musician is None:
                raise ValidationError(
                    "Musician field required when seeking a band"
                )
            if self.band is not None:
                raise ValidationError(
                    (
                        "Band field should be empty for a musician "
                        "seeking a band"
                    )
                )

        super().clean()
