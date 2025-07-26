from django.contrib import admin

from .models import Department, Employee, LeaveType


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    readonly_fields = ('id',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') 
    readonly_fields = ('id',)

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') 
    readonly_fields = ('id',)


