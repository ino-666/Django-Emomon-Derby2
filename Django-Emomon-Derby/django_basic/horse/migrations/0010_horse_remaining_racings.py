# Generated by Django 5.0.6 on 2024-06-24 09:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("horse", "0009_horse_num_remaining_turns"),
    ]

    operations = [
        migrations.AddField(
            model_name="horse",
            name="remaining_racings",
            field=models.IntegerField(default=10),
        ),
    ]
