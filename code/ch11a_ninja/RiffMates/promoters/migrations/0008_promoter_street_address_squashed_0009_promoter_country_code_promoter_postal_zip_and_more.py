# Generated by Django 4.2.2 on 2023-09-19 12:50

from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [
        ("promoters", "0008_promoter_street_address"),
        (
            "promoters",
            "0009_promoter_country_code_promoter_postal_zip_and_more",
        ),
    ]

    dependencies = [
        ("promoters", "0006_promoter_birth_squashed_0007_promoter_death"),
    ]

    operations = [
        migrations.AddField(
            model_name="promoter",
            name="street_address",
            field=models.CharField(default="", max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="promoter",
            name="city",
            field=models.CharField(default="", max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="promoter",
            name="country_code",
            field=models.CharField(default="", max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="promoter",
            name="postal_zip",
            field=models.CharField(default="", max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="promoter",
            name="province_state",
            field=models.CharField(default="", max_length=25),
            preserve_default=False,
        ),
    ]
