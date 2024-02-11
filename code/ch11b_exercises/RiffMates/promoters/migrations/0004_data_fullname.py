# RiffMates/promoter/migrations/0004_data_fullname.py
from django.db import migrations


def de_westernize_names(apps, schema_editor):
    # Can't import Promoter Model, the current version may be newer than the
    # one in this migration. Use historical version instead.
    Promoter = apps.get_model("promoters", "Promoter")
    for promoter in Promoter.objects.all():
        promoter.full_name = f"{promoter.first_name} {promoter.last_name}"
        promoter.common_name = promoter.first_name
        promoter.save()


def re_westernize_names(apps, schema_editor):
    Promoter = apps.get_model("promoters", "Promoter")
    for promoter in Promoter.objects.all():
        promoter.first_name = promoter.common_name
        length = len(promoter.first_name)
        promoter.last_name = promoter.full_name[length + 1 :]

    promoter.save()


class Migration(migrations.Migration):
    dependencies = [
        ("promoters", "0003_promoter_common_name_promoter_full_name"),
    ]

    operations = [
        migrations.RunPython(de_westernize_names, re_westernize_names),
    ]
