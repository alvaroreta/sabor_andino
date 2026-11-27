from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def roles_requeridos(*roles):
    def decorador(view):
        @login_required
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.user.rol not in roles:
                raise PermissionDenied
            return view(request, *args, **kwargs)
        return wrapper
    return decorador
