# Generated by Django 5.0 on 2023-12-06 21:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0002_alter_seekingad_options"),
    ]

    operations = [
        migrations.DeleteModel(
            name="SeekingAd",
        ),
    ]
