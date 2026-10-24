from django.conf import settings
from django.db import models
from django.utils import timezone


class Notificacion(models.Model):
    class Tipo(models.TextChoices):
        CITA = "cita", "Cita"
        RECORDATORIO = "recordatorio", "Recordatorio"
        SISTEMA = "sistema", "Sistema"

    idNotificacion = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notificaciones", db_column="idUsuario")
    titulo = models.CharField(max_length=150)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.SISTEMA)
    leida = models.BooleanField(default=False)
    fechaCreacion = models.DateTimeField(default=timezone.now, editable=False)
    cita = models.ForeignKey("citas.Cita", on_delete=models.SET_NULL, null=True, blank=True, related_name="notificaciones", db_column="idCita")

    class Meta:
        verbose_name = "notificación"
        verbose_name_plural = "notificaciones"
        ordering = ["-fechaCreacion"]

    def __str__(self):
        return f"{self.titulo} - {self.usuario}"


class Configuracion(models.Model):
    idConfig = models.BigAutoField(primary_key=True)
    clave = models.CharField(max_length=100, unique=True)
    valor = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "configuración"
        verbose_name_plural = "configuraciones"
        ordering = ["clave"]

    def __str__(self):
        return f"{self.clave} = {self.valor}"
