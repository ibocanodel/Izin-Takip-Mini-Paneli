from enum import Enum

from leave.constants import Role

default_access_permissions = [Role.NORMAL_EMPLOYEE]


class Page(Enum):
    DEPARTMENTS = "departments"
    LEAVE_TYPES = "leave_types"
    SETTINGS = "settings"
    ADMIN_TASKS = "admin_tasks"
    ALL_LEAVES = "all_leaves"
    EMPLOYEES = "employees"


PAGE_ROLE_ACCESS = {
    Page.ADMIN_TASKS.value: [Role.ADMIN, Role.SUPER_ADMIN],
    Page.DEPARTMENTS.value: [Role.ADMIN, Role.SUPER_ADMIN],
    Page.LEAVE_TYPES.value: [Role.ADMIN, Role.SUPER_ADMIN],
    Page.SETTINGS.value: [Role.SUPER_ADMIN],
    Page.ALL_LEAVES.value: [Role.ADMIN, Role.SUPER_ADMIN],
    Page.EMPLOYEES.value: [Role.ADMIN, Role.SUPER_ADMIN],
}


def get_permissions_of_page(page: Page):
    return PAGE_ROLE_ACCESS.get(page.value, default_access_permissions)
