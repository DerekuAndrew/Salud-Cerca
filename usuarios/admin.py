from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Paciente, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("idUsuario", "correo", "rol", "activo", "fechaRegistro", "last_login")
    list_filter = ("rol", "activo")
    search_fields = ("correo",)
    ordering = ("correo",)
    readonly_fields = ("fechaRegistro", "last_login")
    filter_horizontal = ("groups", "user_permissions")

    fieldsets = (
        (None, {"fields": ("correo", "password")}),
        ("Datos de la cuenta", {"fields": ("rol", "activo", "fechaRegistro", "last_login")}),
        ("Permisos", {"fields": ("is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("correo", "rol", "usable_password", "password1", "password2")}),
    )


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("idPaciente", "nombre", "apellido", "usuario", "telefono", "genero")
    list_filter = ("genero",)
    search_fields = ("nombre", "apellido", "usuario__correo", "telefono")
    list_select_related = ("usuario",)
