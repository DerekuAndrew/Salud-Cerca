from django.contrib import admin
from .models import Cita, Resena


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ("idCita", "paciente", "doctor", "especialidad", "fechaCita", "horaInicio", "estado")
    list_filter = ("estado", "fechaCita", "especialidad")
    search_fields = ("paciente__nombre", "paciente__apellido", "doctor__nombre", "doctor__apellido")
    list_select_related = ("paciente", "doctor", "especialidad")
    date_hierarchy = "fechaCita"


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ("doctor", "paciente", "calificacion", "fecha", "visible")
    list_filter = ("calificacion", "visible", "fecha")
    search_fields = ("doctor__nombre", "paciente__nombre", "comentario")
    list_select_related = ("doctor", "paciente", "cita")
