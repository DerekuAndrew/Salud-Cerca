from django.conf import settings
from django.db import models
from django.utils import timezone


class Cita(models.Model):
    class Estado(models.TextChoices):
        SOLICITADA = "solicitada", "Solicitada"
        CONFIRMADA = "confirmada", "Confirmada"
        CANCELADA = "cancelada", "Cancelada"
        COMPLETADA = "completada", "Completada"
        NO_ASISTIO = "no_asistio", "No asistió"

    idCita = models.BigAutoField(primary_key=True)
    paciente = models.ForeignKey("usuarios.Paciente", on_delete=models.PROTECT, related_name="citas", db_column="idPaciente")
    doctor = models.ForeignKey("medicos.Doctor", on_delete=models.PROTECT, related_name="citas", db_column="idDoctor")
    especialidad = models.ForeignKey("medicos.Especialidad", on_delete=models.PROTECT, related_name="citas", db_column="idEspecialidad")
    fechaCita = models.DateField()
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.SOLICITADA)
    motivoConsulta = models.TextField(blank=True)
    notasDoctor = models.TextField(blank=True)
    fechaSolicitud = models.DateTimeField(default=timezone.now, editable=False)
    fechaActualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "cita"
        verbose_name_plural = "citas"
        ordering = ["-fechaCita", "horaInicio"]
        constraints = [models.CheckConstraint(condition=models.Q(horaFin__gt=models.F("horaInicio")), name="ck_cita_fin_mayor_inicio")]

    def __str__(self):
        return f"Cita #{self.idCita} - {self.paciente} - {self.fechaCita}"


class Resena(models.Model):
    idResena = models.BigAutoField(primary_key=True)
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE, related_name="resena", db_column="idCita")
    paciente = models.ForeignKey("usuarios.Paciente", on_delete=models.PROTECT, related_name="resenas", db_column="idPaciente")
    doctor = models.ForeignKey("medicos.Doctor", on_delete=models.PROTECT, related_name="resenas", db_column="idDoctor")
    calificacion = models.PositiveSmallIntegerField()
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = "reseña"
        verbose_name_plural = "reseñas"
        ordering = ["-fecha"]
        constraints = [models.CheckConstraint(condition=models.Q(calificacion__gte=1, calificacion__lte=5), name="ck_resena_calificacion_1_5")]

    def __str__(self):
        return f"Reseña {self.calificacion}/5 - {self.doctor}"
