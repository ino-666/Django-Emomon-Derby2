# Generated by Django 5.0.6 on 2024-06-25 02:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_remove_training_race_delete_race_delete_training"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="ed_enables",
            field=models.BooleanField(default=False),
        ),
    ]
