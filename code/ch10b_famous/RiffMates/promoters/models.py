# RiffMates/promoters/models.py
from django.db import models


class Promoter(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    famous_for = models.CharField(max_length=50)
