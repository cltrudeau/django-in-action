# Generated by Django 5.0 on 2023-12-06 21:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "promoters",
            "0012_remove_promoter_city_remove_promoter_country_code_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="promoter",
            name="address",
            field=models.TextField(blank=True, default=""),
        ),
    ]