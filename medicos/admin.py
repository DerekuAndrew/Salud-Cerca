from django.contrib import admin

from .models import CentroMedico, Doctor, DoctorEspecialidad, Especialidad, ExcepcionHorario, Horario


class DoctorEspecialidadInline(admin.TabularInline):
    model = DoctorEspecialidad
    extra = 1


class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 0


@admin.register(CentroMedico)
class CentroMedicoAdmin(admin.ModelAdmin):
    list_display = ("idCentro", "nombre", "ciudad", "telefono", "activo")
    list_filter = ("ciudad", "activo")
    search_fields = ("nombre", "ciudad", "direccion")


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("idEspecialidad", "nombre", "icono")
    search_fields = ("nombre",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("idDoctor", "nombre", "apellido", "cedulaProfesional", "centro", "activo")
    list_filter = ("activo", "centro", "especialidades")
    search_fields = ("nombre", "apellido", "cedulaProfesional", "usuario__correo")
    list_select_related = ("centro", "usuario")
    inlines = [DoctorEspecialidadInline, HorarioInline]


@admin.register(DoctorEspecialidad)
class DoctorEspecialidadAdmin(admin.ModelAdmin):
    list_display = ("idDoctorEspecialidad", "doctor", "especialidad")
    list_select_related = ("doctor", "especialidad")


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ("idHorario", "doctor", "diaSemana", "horaInicio", "horaFin", "duracionCita")
    list_filter = ("diaSemana",)
    list_select_related = ("doctor",)


@admin.register(ExcepcionHorario)
class ExcepcionHorarioAdmin(admin.ModelAdmin):
    list_display = ("idExcepcion", "doctor", "fecha", "todoElDia", "horaInicio", "horaFin", "motivo")
    list_filter = ("todoElDia", "fecha")
    list_select_related = ("doctor",)
