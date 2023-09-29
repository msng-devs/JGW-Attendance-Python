# Generated by Django 4.2.4 on 2023-09-28 08:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("attendance", "0003_alter_attendance_created_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance",
            name="created_by",
            field=models.CharField(
                default="system", max_length=30, verbose_name="Created By"
            ),
        ),
        migrations.AlterField(
            model_name="attendance",
            name="modified_by",
            field=models.CharField(
                default="system", max_length=30, verbose_name="Modified By"
            ),
        ),
        migrations.AlterField(
            model_name="attendancetype",
            name="created_by",
            field=models.CharField(
                default="system", max_length=30, verbose_name="Created By"
            ),
        ),
        migrations.AlterField(
            model_name="attendancetype",
            name="modified_by",
            field=models.CharField(
                default="system", max_length=30, verbose_name="Modified By"
            ),
        ),
    ]