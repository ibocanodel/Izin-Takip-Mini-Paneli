from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from leave.constants import Role
from leave.decorators import role_required
from leave.forms.leave_type import LeaveTypeForm
from leave.models import Leave, LeaveType
from leave.permissions import Page
from leave.utils import user_has_roles

PAGE_ENUM = Page.LEAVE_TYPES


@role_required(PAGE_ENUM)
def leave_type_list(request):
    if not user_has_roles(request, [Role.ADMIN, Role.SUPER_ADMIN]):
        return HttpResponseForbidden("Bu sayfayı görüntüleme yetkiniz yok.")
    types = LeaveType.objects.filter(is_deleted=False)
    return render(request, "leave_type/leave_type_listing.html", {"types": types})


@role_required(PAGE_ENUM)
def add_leave_type(request):
    if not user_has_roles(request, [Role.ADMIN, Role.SUPER_ADMIN]):
        return HttpResponseForbidden("Bu sayfayı görüntüleme yetkiniz yok.")
    if request.method == "POST":
        form = LeaveTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("leave_type_list")
    else:
        form = LeaveTypeForm()
    return render(request, "leave_type/leave_type_add.html", {"form": form})


@role_required(PAGE_ENUM)
def edit_leave_type(request, pk):
    leave_type = get_object_or_404(LeaveType, pk=pk)
    form = LeaveTypeForm(request.POST or None, instance=leave_type)
    if form.is_valid():
        form.save()
        return redirect("leave_type_list")
    return render(request, "leave_type/leave_type_edit.html", {"form": form})


@role_required(PAGE_ENUM)
def delete_leave_type(request, pk):
    if (
        request.method == "POST"
        and request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        leave_type = get_object_or_404(LeaveType, pk=pk)
        has_leave = Leave.objects.filter(leave_type=leave_type).exists()
        if has_leave:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Bu tipte geçmişte izin alındığı için silenemez",
                },
                status=400,
            )
        leave_type.is_deleted = True
        leave_type.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)
