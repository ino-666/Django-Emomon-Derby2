

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("horse", "0004_trait_cpu_horse_traits_horse_traits"),
    ]

    operations = [
        migrations.AlterField(
            model_name="horse",
            name="luck_increase",
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name="horse",
            name="speed_increase",
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name="horse",
            name="stamina_increase",
            field=models.IntegerField(default=-1),
        ),
    ]
