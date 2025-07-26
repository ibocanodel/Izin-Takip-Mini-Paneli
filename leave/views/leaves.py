from datetime import datetime
from urllib.parse import urlencode

from django.contrib import messages
from django.db.models.functions import ExtractYear
from django.http import JsonResponse
from django.shortcuts import redirect, render

from leave.decorators import role_required
from leave.forms.leave import LeaveForm
from leave.models import AppSettings, Department, Employee, Leave, LeaveType
from leave.permissions import Page
from django.core.paginator import Paginator

ALL_LEAVES_LIST_PAGE_ENUM = Page.ALL_LEAVES


def leave_request(request):
    app_settings = AppSettings.objects.first()
    employee_id = request.session.get("employee_id")
    current_employee = Employee.objects.get(id=employee_id)
    if request.method == "POST":
        form = LeaveForm(
            request.POST,
            employee=current_employee,
            force_submit=request.POST.get("force_submit") == "true",
        )

        if form.is_valid():
            leave = form.save(commit=False)

            leave.employee_id = employee_id
            leave.save()
            return redirect("leave_list")
        else:
            all_errors = []
            none_errors = []
        print(f"tt {form.errors}")
        for field, errors in form.errors.items():
            if field == "__all__":
                for error in errors:
                    none_errors.append(f"{error}")
            else:
                for error in errors:
                    all_errors.append(f"{error}")
        if len(all_errors) == 0 and len(none_errors) > 0:
            return JsonResponse(
                {
                    "success": False,
                    "error": " | ".join(none_errors),
                    "input_required": True,
                }
            )
        messages.error(request, " | ".join(all_errors))

    leave_types = LeaveType.objects.filter(is_deleted=False)
    working_days = [1, 2, 3, 4, 5]

    if app_settings and app_settings.work_days:
        working_days = list(map(int, app_settings.work_days.split(",")))
    return render(
        request,
        "leave_request.html",
        {
            "leave_types": leave_types,
            "work_days": working_days,
            "employee": current_employee,
        },
    )


def all_leaves_view(request):
    employees = Employee.objects.all()
    departments = Department.objects.all()
    query_params = request.GET.copy()

    page_size = int(query_params.get("page_size", 20))
    page_number = query_params.get("page", 1)
    page_size_options = [5, 10, 20, 50, 100]

    leaves = Leave.objects.select_related(
        "employee", "leave_type", "employee__department"
    ).filter(is_deleted=False)

    employee_id = query_params.get("employee")
    department_id = query_params.get("department")
    start_date = query_params.get("start_date")
    end_date = query_params.get("end_date")

    if employee_id:
        leaves = leaves.filter(employee_id=employee_id)
    if department_id:
        leaves = leaves.filter(employee__department_id=department_id)
    if start_date and end_date:
        leaves = leaves.filter(start_date__lte=end_date, end_date__gte=start_date)
    elif start_date:
        leaves = leaves.filter(end_date__gte=start_date)
    elif end_date:
        leaves = leaves.filter(start_date__lte=end_date)

    leaves = leaves.order_by("start_date")

    paginator = Paginator(leaves, page_size)
    page_obj = paginator.get_page(page_number)

    query_params.pop("page", None)

    context = {
        "page_obj": page_obj,
        "employees": employees,
        "departments": departments,
        "filters": {
            "employee_id": employee_id,
            "department_id": department_id,
            "start_date": start_date,
            "end_date": end_date,
        },
        "query_string": urlencode(query_params),
        "page_size": page_size,
        "page_size_options": page_size_options,
    }

    return render(request, "all_leaves.html", context)


def leave_list(request):
    current_employee_id = request.session.get("employee_id")
    selected_year = request.GET.get("year")
    page_number = request.GET.get("page")
    page_size = request.GET.get("page_size", 10)

    try:
        page_size = int(page_size)
    except ValueError:
        page_size = 10

    leaves = Leave.objects.filter(employee_id=current_employee_id, is_deleted=False)

    if selected_year:
        leaves = leaves.filter(start_date__year=selected_year)

    leaves = leaves.order_by("start_date")

    paginator = Paginator(leaves, page_size)
    page_obj = paginator.get_page(page_number)

    years = (
        Leave.objects.filter(employee_id=current_employee_id, is_deleted=False)
        .annotate(year=ExtractYear("start_date"))
        .values_list("year", flat=True)
        .distinct()
        .order_by("-year")
    )

    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")
    page_size_options = [5, 10, 20, 50, 100]

    return render(
        request,
        "employee_own_leave_list.html",
        {
            "page_obj": page_obj,
            "years": years,
            "selected_year": selected_year or str(datetime.now().year),
            "page_size": page_size,
            "query_string": urlencode(query_params),
            "page_size_options": page_size_options,
        },
    )
