from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("promoters", "0002_promoter_famous_for"),
    ]

    operations = [
        migrations.AddField(
            model_name="promoter",
            name="common_name",
            field=models.CharField(default="", max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="promoter",
            name="full_name",
            field=models.CharField(default="", max_length=50),
            preserve_default=False,
        ),
    ]
