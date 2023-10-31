from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("promoter", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="promoter",
            name="famous_for",
            field=models.CharField(default="", max_length=50),
            preserve_default=False,
        ),
    ]
