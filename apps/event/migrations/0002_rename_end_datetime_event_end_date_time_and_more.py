# Generated by Django 4.2.4 on 2023-09-03 16:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("event", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="end_datetime",
            new_name="end_date_time",
        ),
        migrations.RenameField(
            model_name="event",
            old_name="start_datetime",
            new_name="start_date_time",
        ),
    ]
