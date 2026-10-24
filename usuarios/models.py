from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UsuarioManager(BaseUserManager):
    """Manager para el usuario personalizado (inicia sesión con el correo)."""

    use_in_migrations = True

    def _crear(self, correo, password, **extra):
        if not correo:
            raise ValueError("El correo es obligatorio.")
        correo = self.normalize_email(correo)
        usuario = self.model(correo=correo, **extra)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_user(self, correo, password=None, **extra):
        extra.setdefault("rol", Usuario.Rol.PACIENTE)
        return self._crear(correo, password, **extra)

    def create_superuser(self, correo, password=None, **extra):
        extra.setdefault("rol", Usuario.Rol.ADMIN)
        extra["is_superuser"] = True
        return self._crear(correo, password, **extra)


class Usuario(AbstractBaseUser, PermissionsMixin):
    """Tabla `usuario` del diagrama (cuenta de acceso al sistema)."""

    class Rol(models.TextChoices):
        PACIENTE = "paciente", "Paciente"
        DOCTOR = "doctor", "Doctor"
        ADMIN = "admin", "Administrador"

    idUsuario = models.BigAutoField(primary_key=True)
    correo = models.EmailField(unique=True)
    # passwordHash: Django ya guarda aquí la contraseña con hash.
    password = models.CharField("passwordHash", max_length=128, db_column="passwordHash")
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.PACIENTE)
    fechaRegistro = models.DateTimeField(default=timezone.now, editable=False)
    activo = models.BooleanField(default=True)
    # ultimoAcceso: es el last_login de Django.
    last_login = models.DateTimeField("último acceso", null=True, blank=True, db_column="ultimoAcceso")

    objects = UsuarioManager()

    USERNAME_FIELD = "correo"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        ordering = ["correo"]

    @property
    def is_active(self):
        return self.activo

    @property
    def is_staff(self):
        # Entra al panel de administración quien sea admin o superusuario.
        return self.is_superuser or self.rol == self.Rol.ADMIN

    def __str__(self):
        return self.correo


class Paciente(models.Model):
    """Tabla `paciente` (relación 1 a 1 con usuario)."""

    class Genero(models.TextChoices):
        FEMENINO = "F", "Femenino"
        MASCULINO = "M", "Masculino"
        OTRO = "O", "Otro"

    idPaciente = models.BigAutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="paciente", db_column="idUsuario")
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    fechaNacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=Genero.choices, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "paciente"
        verbose_name_plural = "pacientes"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
