# Generated by Django 4.1.5 on 2023-05-18 16:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bands", "0005_alter_userprofile_musician_profiles_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="venue",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="venue",
            name="picture",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]