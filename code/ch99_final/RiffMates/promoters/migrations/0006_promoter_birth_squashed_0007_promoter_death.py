from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [
        ("promoters", "0006_promoter_birth"),
        ("promoters", "0007_promoter_death"),
    ]

    dependencies = [
        (
            "promoters",
            "0005_remove_promoter_first_name_remove_promoter_last_name",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="promoter",
            name="birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="promoter",
            name="death",
            field=models.DateField(blank=True, null=True),
        ),
    ]
