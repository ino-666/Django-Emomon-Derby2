# Generated by Django 5.0.6 on 2024-06-12 07:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("race", "0002_cpu_horse_horse_delete_cpuhorce_delete_horce"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CPU_Horse",
        ),
        migrations.DeleteModel(
            name="Horse",
        ),
    ]
