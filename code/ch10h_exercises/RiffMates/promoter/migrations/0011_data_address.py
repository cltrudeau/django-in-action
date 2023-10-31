# RiffMates/promoter/migrations/0011_data_address.py
from django.db import migrations


def group_address(apps, schema_editor):
    Promoter = apps.get_model("promoter", "Promoter")
    for promoter in Promoter.objects.all():
        text = ""
        if promoter.street_address:
            text += promoter.street_address + "\n"
        if promoter.city:
            text += promoter.city + "\n"
        if promoter.province_state:
            text += promoter.province_state + "\n"
        if promoter.country_code:
            text += promoter.country_code + "\n"
        if promoter.postal_zip:
            text += promoter.postal_zip + "\n"

        promoter.address = text
        promoter.save()


class Migration(migrations.Migration):
    dependencies = [
        (
            "promoter",
            "0010_promoter_address",
        ),
    ]

    operations = [
        # Can't undo this migration, there is no way of which lines were
        # missing in the grouping
        migrations.RunPython(group_address),
    ]
