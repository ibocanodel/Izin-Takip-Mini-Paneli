from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from leave.decorators import role_required
from leave.forms.user import CreateEmployeeForm, UpdateEmployeeForm
from leave.models import AppSettings, Employee
from leave.permissions import Page

PAGE_ENUM = Page.EMPLOYEES


@role_required(PAGE_ENUM)
def create_employee(request):
    settings_obj = AppSettings.objects.get()
    if request.method == "POST":
        form = CreateEmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)

            employee.password = make_password(settings_obj.default_password)
            employee.save()
            messages.success(request, "Yeni çalışan başarıyla oluşturuldu.")
            return redirect("employee_list")
    else:
        form = CreateEmployeeForm()

    return render(
        request,
        "employee/create_employee.html",
        {"form": form, "default_password": settings_obj.default_password},
    )


@role_required(PAGE_ENUM)
def employee_list(request):
    employees = Employee.objects.filter()
    query_params = request.GET.copy()
    page_number = request.GET.get("page")
    page_size = request.GET.get("page_size", 10)
    paginator = Paginator(employees, page_size)
    page_obj = paginator.get_page(page_number)
    page_size_options = [1, 5, 10, 20, 50, 100]
    query_params.pop("page", None)

    try:
        page_size = int(page_size)
    except ValueError:
        page_size = 10
    return render(
        request,
        "employee/employee_list.html",
        {
            "employees": employees,
            "page_obj": page_obj,
            "query_string": urlencode(query_params),
            "page_size": page_size,
            "page_size_options": page_size_options,
        },
    )


@role_required(PAGE_ENUM)
def update_employee(request, pk):

    employee = get_object_or_404(Employee, pk=pk, is_deleted=False)
    if request.method == "POST":
        form = UpdateEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            updated_employee = form.save(commit=False)
            updated_employee.save()
            return redirect("employees")
    else:
        form = UpdateEmployeeForm(instance=employee)

    return render(
        request, "employee/update_employee.html", {"form": form, "employee": employee}
    )
