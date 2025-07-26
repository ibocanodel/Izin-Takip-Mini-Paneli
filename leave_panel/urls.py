"""
URL configuration for leave_panel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.shortcuts import render
from django.urls import path

from leave.views import admin as adminoops
from leave.views import department, employees, leave_type, leaves, user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", user.user_login, name="login"),
    path("logout/", user.user_logout, name="logout"),
    path("", user.user_login, name="login"),
    path("home/", leaves.leave_list, name="leave_list"),
    path("izin-al/", leaves.leave_request, name="leave_request"),
    path("izin-turleri/", leave_type.leave_type_list, name="leave_type_list"),
    path("izin-turleri/ekle/", leave_type.add_leave_type, name="add_leave_type"),
    path(
        "izin-turleri/<int:pk>/duzenle/",
        leave_type.edit_leave_type,
        name="edit_leave_type",
    ),
    path(
        "izin-turleri/<int:pk>/sil/",
        leave_type.delete_leave_type,
        name="delete_leave_type",
    ),
    path("departman-turleri/", department.department_list, name="department_list"),
    path("departman/ekle/", department.add_department, name="add_department"),
    path(
        "departman/<int:pk>/duzenle/",
        department.edit_department,
        name="edit_department",
    ),
    path(
        "departman/<int:pk>/sil/",
        department.delete_department,
        name="delete_department",
    ),
    path("izinler/tumu/", leaves.all_leaves_view, name="all_leaves"),
    path("profilim/", user.my_profile, name="my_profile"),
    path("calisan/ekle/", employees.create_employee, name="create_employee"),
    path("calisan", employees.employee_list, name="employees"),
    path("settings/", adminoops.update_settings, name="update_settings"),
    path(
        "calisan/<int:pk>/duzenle/", employees.update_employee, name="update_employee"
    ),
]


def custom_404_view(request, exception):
    return render(request, "page_not_found.html", status=404)


handler404 = "leave_panel.urls.custom_404_view"
