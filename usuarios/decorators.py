from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

##-- Seguridad
def roles_requeridos(*roles):
    def decorador(view):
        ##-- Recibe los roles permitidos
        @login_required
        ##-- filtra vista por rol recibido
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            ##-- si el rol del usuario no se encuentra habilitado en la vista por rol se le denega el acceso
            if request.user.rol not in roles:
                raise PermissionDenied
            return view(request, *args, **kwargs)
        return wrapper
    return decorador
