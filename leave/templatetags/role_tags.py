from django import template

from leave.permissions import PAGE_ROLE_ACCESS, default_access_permissions

register = template.Library()


@register.filter
def can_access(user, page_enum):
    try:
        allowed_roles = PAGE_ROLE_ACCESS.get(page_enum, default_access_permissions)
        return user.role in allowed_roles
    except Exception:
        return False