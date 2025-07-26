from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from leave.constants import Role
from leave.decorators import role_required
from leave.forms.department import DepartmentForm
from leave.models import Department, Employee
from leave.utils import user_has_roles
from leave.permissions import Page


PAGE_ENUM = Page.DEPARTMENTS

@role_required(PAGE_ENUM)
def department_list(request):
    departments = Department.objects.filter(is_deleted=False)
    return render(request, 'department/department_listing.html', {'types': departments})

@role_required(PAGE_ENUM)
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'department_add.html', {'form': form})

@role_required(PAGE_ENUM)
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=department)
    if form.is_valid():
        form.save()
        return redirect('department_list')
    return render(request, 'department/department_edit.html', {'form': form})

@role_required(PAGE_ENUM)
def delete_department(request, pk):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        department = get_object_or_404(Department, pk=pk)
        has_employees = Employee.objects.filter(department=department).exists()
        if has_employees:
            return JsonResponse({
                "success": False,
                "error": "Bu departmana bağlı çalışanlar olduğu için silinemez."
            }, status=400)
        department.is_deleted = True
        department.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)