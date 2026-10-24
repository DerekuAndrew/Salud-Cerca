from django.contrib import admin

from .models import Configuracion, Notificacion


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ("idNotificacion", "usuario", "titulo", "tipo", "leida", "fechaCreacion")
    list_filter = ("tipo", "leida", "fechaCreacion")
    search_fields = ("titulo", "mensaje", "usuario__correo")
    list_select_related = ("usuario", "cita")


@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    list_display = ("idConfig", "clave", "valor", "descripcion")
    search_fields = ("clave", "descripcion")
