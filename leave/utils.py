from typing import List

from leave.constants import Role
from leave.permissions import Page


def user_has_roles(request, roles : List[Role]):

    employee_id = request.session.get("employee_id")
    if not employee_id:
        return False
    from .models import Employee
    try:
        employee = Employee.objects.get(id=employee_id)
        return employee.role in roles
    except Employee.DoesNotExist:
        return False