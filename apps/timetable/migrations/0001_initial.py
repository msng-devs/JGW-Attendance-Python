# Generated by Django 4.2.4 on 2023-09-03 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("event", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TimeTable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_datetime",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created Date Time"
                    ),
                ),
                (
                    "modified_datetime",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Modified Date Time"
                    ),
                ),
                (
                    "created_by",
                    models.CharField(max_length=30, verbose_name="Created By"),
                ),
                (
                    "modified_by",
                    models.CharField(max_length=30, verbose_name="Modified By"),
                ),
                (
                    "name",
                    models.CharField(max_length=50, verbose_name="Time Table Name"),
                ),
                (
                    "index",
                    models.TextField(max_length=200, verbose_name="Time Table Index"),
                ),
                (
                    "start_datetime",
                    models.DateTimeField(verbose_name="Time Table Start DateTime"),
                ),
                (
                    "end_datetime",
                    models.DateTimeField(verbose_name="Time Table End DateTime"),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="event.event",
                        verbose_name="Related Event",
                    ),
                ),
            ],
            options={
                "verbose_name": "Time Table",
                "verbose_name_plural": "Time Tables",
                "db_table": "time_table",
            },
        ),
    ]
