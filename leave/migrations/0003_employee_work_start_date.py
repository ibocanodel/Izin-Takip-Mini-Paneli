# Generated by Django 5.2.4 on 2025-07-25 11:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leave", "0002_remove_employee_is_admin_employee_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="work_start_date",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
