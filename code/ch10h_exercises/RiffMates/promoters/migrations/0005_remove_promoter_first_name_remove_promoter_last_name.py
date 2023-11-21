from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("promoters", "0004_data_fullname"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="promoter",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="promoter",
            name="last_name",
        ),
    ]
