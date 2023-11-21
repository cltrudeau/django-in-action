from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("promoters", "0006_promoter_birth"),
    ]

    operations = [
        migrations.AddField(
            model_name="promoter",
            name="death",
            field=models.DateField(blank=True, null=True),
        ),
    ]
