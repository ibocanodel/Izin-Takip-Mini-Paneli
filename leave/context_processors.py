from leave.permissions import Page

from .models import Employee


def employee_context(request):
    employee_id = request.session.get("employee_id")
    if employee_id:
        try:
            employee = Employee.objects.get(id=employee_id)
            return {"current_employee": employee}
        except Employee.DoesNotExist:
            pass
    return {"current_employee": None}

def page_enums(request):
    return {"Page": Page}
