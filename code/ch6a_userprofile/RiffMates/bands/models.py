# RiffMates/bands/models.py
from django.contrib.auth.models import User
from django.db import models


class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth = models.DateField()

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"Musician(id={self.id}, last_name={self.last_name})"


class Band(models.Model):
    name = models.CharField(max_length=20)
    musicians = models.ManyToManyField(Musician)

    class Meta:
        ordering = [
            "name",
        ]

    def __str__(self):
        return f"Band(id={self.id}, name={self.name})"


class Venue(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = [
            "name",
        ]

    def __str__(self):
        return f"Venue(id={self.id}, name={self.name})"


class Room(models.Model):
    name = models.CharField(max_length=20)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    class Meta:
        ordering = [
            "name",
        ]

    def __str__(self):
        return f"Room(id={self.id}, name={self.name})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    musician_profiles = models.ManyToManyField(Musician, blank=True)
    venues_controlled = models.ManyToManyField(Venue, blank=True)
