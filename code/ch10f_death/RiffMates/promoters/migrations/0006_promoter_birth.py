from django.db import migrations, models


class Migration(migrations.Migration):
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
    ]
