from django.conf import settings
from django.db import models


class CentroMedico(models.Model):
    idCentro = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "centro médico"
        verbose_name_plural = "centros médicos"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"


class Especialidad(models.Model):
    idEspecialidad = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "especialidad"
        verbose_name_plural = "especialidades"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Doctor(models.Model):
    idDoctor = models.BigAutoField(primary_key=True)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor", db_column="idUsuario")
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    cedulaProfesional = models.CharField(max_length=30, unique=True)
    biografia = models.TextField(blank=True)
    centro = models.ForeignKey(CentroMedico, on_delete=models.PROTECT, related_name="doctores", db_column="idCentro")
    activo = models.BooleanField(default=True)
    # La tabla intermedia doctorEspecialidad del diagrama se modela con "through".
    especialidades = models.ManyToManyField(Especialidad, through="DoctorEspecialidad", related_name="doctores")

    class Meta:
        verbose_name = "doctor"
        verbose_name_plural = "doctores"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido}"


class DoctorEspecialidad(models.Model):
    idDoctorEspecialidad = models.BigAutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_especialidades", db_column="idDoctor")
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name="doctor_especialidades", db_column="idEspecialidad")

    class Meta:
        verbose_name = "especialidad del doctor"
        verbose_name_plural = "especialidades de los doctores"
        constraints = [models.UniqueConstraint(fields=["doctor", "especialidad"], name="uq_doctor_especialidad")]

    def __str__(self):
        return f"{self.doctor} - {self.especialidad}"


class Horario(models.Model):
    class DiaSemana(models.IntegerChoices):
        LUNES = 0, "Lunes"
        MARTES = 1, "Martes"
        MIERCOLES = 2, "Miércoles"
        JUEVES = 3, "Jueves"
        VIERNES = 4, "Viernes"
        SABADO = 5, "Sábado"
        DOMINGO = 6, "Domingo"

    idHorario = models.BigAutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="horarios", db_column="idDoctor")
    diaSemana = models.PositiveSmallIntegerField(choices=DiaSemana.choices)
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    duracionCita = models.PositiveSmallIntegerField(default=30, help_text="Duración de cada cita en minutos.")

    class Meta:
        verbose_name = "horario"
        verbose_name_plural = "horarios"
        ordering = ["doctor", "diaSemana", "horaInicio"]
        constraints = [models.CheckConstraint(condition=models.Q(horaFin__gt=models.F("horaInicio")), name="ck_horario_fin_mayor_inicio")]

    def __str__(self):
        return f"{self.doctor} - {self.get_diaSemana_display()} {self.horaInicio:%H:%M}-{self.horaFin:%H:%M}"


class ExcepcionHorario(models.Model):
    idExcepcion = models.BigAutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="excepciones", db_column="idDoctor")
    fecha = models.DateField()
    todoElDia = models.BooleanField(default=True)
    horaInicio = models.TimeField(null=True, blank=True)
    horaFin = models.TimeField(null=True, blank=True)
    motivo = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "excepción de horario"
        verbose_name_plural = "excepciones de horario"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.doctor} - {self.fecha}"
