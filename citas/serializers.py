from django.utils import timezone
from rest_framework import serializers

from .models import Cita, Resena


def _valor(serializer, attrs, campo):
    """Valor nuevo si viene en la petición; si no, el que ya tiene el objeto (PATCH)."""
    return attrs.get(campo, getattr(serializer.instance, campo, None))


class CitaSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.StringRelatedField(source="paciente", read_only=True)
    doctor_nombre = serializers.StringRelatedField(source="doctor", read_only=True)
    especialidad_nombre = serializers.StringRelatedField(source="especialidad", read_only=True)

    class Meta:
        model = Cita
        fields = [
            "idCita", "paciente", "paciente_nombre", "doctor", "doctor_nombre",
            "especialidad", "especialidad_nombre", "fechaCita", "horaInicio", "horaFin",
            "estado", "motivoConsulta", "notasDoctor", "fechaSolicitud", "fechaActualizacion",
        ]
        read_only_fields = ["idCita", "fechaSolicitud", "fechaActualizacion"]

    def validate(self, attrs):
        doctor = _valor(self, attrs, "doctor")
        especialidad = _valor(self, attrs, "especialidad")
        fecha = _valor(self, attrs, "fechaCita")
        inicio = _valor(self, attrs, "horaInicio")
        fin = _valor(self, attrs, "horaFin")
        estado = _valor(self, attrs, "estado") or Cita.Estado.SOLICITADA
        es_nueva = self.instance is None

        # La base de datos tiene un CheckConstraint; aquí damos un error 400 claro.
        if inicio and fin and fin <= inicio:
            raise serializers.ValidationError({"horaFin": "La hora de fin debe ser mayor que la de inicio."})

        if es_nueva and fecha and fecha < timezone.localdate():
            raise serializers.ValidationError({"fechaCita": "No se puede agendar una cita en una fecha pasada."})

        if doctor and (es_nueva or "doctor" in attrs) and not doctor.activo:
            raise serializers.ValidationError({"doctor": "El doctor no está activo."})

        if doctor and especialidad and (es_nueva or "doctor" in attrs or "especialidad" in attrs):
            if not doctor.especialidades.filter(pk=especialidad.pk).exists():
                raise serializers.ValidationError(
                    {"especialidad": "El doctor seleccionado no tiene esa especialidad."}
                )

        # Un doctor no puede tener dos citas activas encimadas.
        if estado != Cita.Estado.CANCELADA and doctor and fecha and inicio and fin:
            choques = Cita.objects.filter(
                doctor=doctor, fechaCita=fecha, horaInicio__lt=fin, horaFin__gt=inicio,
            ).exclude(estado=Cita.Estado.CANCELADA)
            if self.instance:
                choques = choques.exclude(pk=self.instance.pk)
            if choques.exists():
                raise serializers.ValidationError("El doctor ya tiene una cita en ese horario.")

        return attrs


class ResenaSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.StringRelatedField(source="paciente", read_only=True)
    doctor_nombre = serializers.StringRelatedField(source="doctor", read_only=True)

    class Meta:
        model = Resena
        fields = [
            "idResena", "cita", "paciente", "paciente_nombre", "doctor", "doctor_nombre",
            "calificacion", "comentario", "fecha", "visible",
        ]
        read_only_fields = ["idResena"]
        extra_kwargs = {"calificacion": {"min_value": 1, "max_value": 5}}

    def validate(self, attrs):
        cita = _valor(self, attrs, "cita")
        paciente = _valor(self, attrs, "paciente")
        doctor = _valor(self, attrs, "doctor")

        if cita:
            if paciente and cita.paciente_id != paciente.pk:
                raise serializers.ValidationError({"paciente": "El paciente no corresponde a la cita."})
            if doctor and cita.doctor_id != doctor.pk:
                raise serializers.ValidationError({"doctor": "El doctor no corresponde a la cita."})
            if self.instance is None and cita.estado != Cita.Estado.COMPLETADA:
                raise serializers.ValidationError({"cita": "Solo se puede reseñar una cita completada."})
        return attrs
