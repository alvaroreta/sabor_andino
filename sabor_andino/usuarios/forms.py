from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class UsuarioForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'dni', 'telefono',
                  'direccion', 'rol', 'foto_perfil')
