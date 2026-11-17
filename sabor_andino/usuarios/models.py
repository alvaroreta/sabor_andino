from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe ingresar un e-mail válido.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('rol', 'SOCIO_GERENTE')
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    class Roles(models.TextChoices):
        SOCIO_GERENTE = 'SOCIO_GERENTE', 'Socio Gerente'
        ACOPIADOR = 'ACOPIADOR', 'Acopiador (Cachi)'
        AUX_LABORATORIO = 'AUX_LABORATORIO', 'Auxiliar de Laboratorio'
        RESP_CALIDAD = 'RESP_CALIDAD', 'Responsable de Calidad'
        ENC_DEPOSITO = 'ENC_DEPOSITO', 'Encargado de Deposito'
        JEFA_PLANTA = 'JEFA_PLANTA', 'Jefa de Planta'

    username = None

    email = models.EmailField('Correo electrónico', unique=True)
    dni = models.CharField('DNI', max_length=15, unique=True)
    telefono = models.CharField('Teléfono', max_length=25, blank=True)
    direccion = models.CharField('Dirección', max_length=150, blank=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    rol = models.CharField(
        'Rol',
        max_length=20,
        choices=Roles.choices,
        default=Roles.ACOPIADOR
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'dni']

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_rol_display()})"
