from datetime import datetime
from django.apps import AppConfig
from django.contrib.auth.hashers import make_password
import os

from leave.constants import Role


class Settonfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "leave"

    def ready(self):
        from django.db.utils import OperationalError

        from .models import AppSettings, Employee, Department, LeaveType

        try:
            AppSettings.objects.get_or_create(pk=1)
            default_departments = os.getenv("DEFAULT_DEPARTMENTS", "")
            employees_raw = os.getenv("DEFAULT_EMPLOYEES")
            password = os.getenv("DEFAULT_PASSWORD")
            default_leave_types = os.getenv("DEFAULT_LEAVE_TYPES")
            default_leave_count = int(os.getenv("DEFAULT_LEAVE_COUNT", 20))
            if default_departments:
                department_names = [
                    name.strip()
                    for name in default_departments.split(",")
                    if name.strip()
                ]
                for name in department_names:
                    Department.objects.get_or_create(name=name)
            if employees_raw and password:
                employee_pairs = employees_raw.split(",")
                for pair in employee_pairs:
                    if ":" not in pair:
                        continue
                    name, email = pair.split(":", 1)
                    name = name.strip()
                    email = email.strip()
                    if name and email:
                        Employee.objects.get_or_create(
                            email=email,
                            defaults={
                                "name": name,
                                "role": Role.SUPER_ADMIN,
                                "work_start_date": datetime.now(),
                                "password": make_password(password),
                            },
                        )
            if default_leave_types:
                leave_type_names = [
                    name.strip()
                    for name in default_leave_types.split(",")
                    if name.strip()
                ]
                for name in leave_type_names:
                    LeaveType.objects.get_or_create(
                        name=name, defaults={"annual_leave_days": default_leave_count}
                    )

        except OperationalError:
            pass
