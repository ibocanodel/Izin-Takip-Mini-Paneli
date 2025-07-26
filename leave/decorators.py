
from functools import wraps

from django.http import HttpResponseForbidden

from leave.permissions import Page, get_permissions_of_page
from leave.utils import user_has_roles


def role_required(page_enum: Page):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            roles = get_permissions_of_page(page_enum)
            if not user_has_roles(request, roles):
                return HttpResponseForbidden("Bu sayfayı görüntüleme yetkiniz yok.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
