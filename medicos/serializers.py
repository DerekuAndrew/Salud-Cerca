from rest_framework import serializers

from usuarios.models import Usuario
from .models import CentroMedico, Doctor, DoctorEspecialidad, Especialidad, ExcepcionHorario, Horario


def _valor(serializer, attrs, campo):
    """Valor nuevo si viene en la petición; si no, el que ya tiene el objeto (PATCH)."""
    return attrs.get(campo, getattr(serializer.instance, campo, None))


class CentroMedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroMedico
        fields = ["idCentro", "nombre", "direccion", "ciudad", "telefono", "latitud", "longitud", "activo"]
        read_only_fields = ["idCentro"]

    def validate_latitud(self, valor):
        if valor is not None and not -90 <= valor <= 90:
            raise serializers.ValidationError("La latitud debe estar entre -90 y 90.")
        return valor

    def validate_longitud(self, valor):
        if valor is not None and not -180 <= valor <= 180:
            raise serializers.ValidationError("La longitud debe estar entre -180 y 180.")
        return valor


class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ["idEspecialidad", "nombre", "descripcion", "icono"]
        read_only_fields = ["idEspecialidad"]


class DoctorSerializer(serializers.ModelSerializer):
    centro_nombre = serializers.CharField(source="centro.nombre", read_only=True)
    correo = serializers.EmailField(source="usuario.correo", read_only=True)
    # Solo lectura: las especialidades se asignan en /api/doctor-especialidades/
    especialidades = EspecialidadSerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = [
            "idDoctor", "usuario", "correo", "nombre", "apellido", "telefono",
            "cedulaProfesional", "biografia", "centro", "centro_nombre",
            "activo", "especialidades",
        ]
        read_only_fields = ["idDoctor"]

    def validate_usuario(self, usuario):
        if usuario.rol != Usuario.Rol.DOCTOR:
            raise serializers.ValidationError("El usuario debe tener el rol 'doctor'.")
        return usuario


class DoctorEspecialidadSerializer(serializers.ModelSerializer):
    doctor_nombre = serializers.StringRelatedField(source="doctor", read_only=True)
    especialidad_nombre = serializers.StringRelatedField(source="especialidad", read_only=True)

    class Meta:
        model = DoctorEspecialidad
        fields = ["idDoctorEspecialidad", "doctor", "doctor_nombre", "especialidad", "especialidad_nombre"]
        read_only_fields = ["idDoctorEspecialidad"]


class HorarioSerializer(serializers.ModelSerializer):
    diaSemana_texto = serializers.CharField(source="get_diaSemana_display", read_only=True)

    class Meta:
        model = Horario
        fields = ["idHorario", "doctor", "diaSemana", "diaSemana_texto", "horaInicio", "horaFin", "duracionCita"]
        read_only_fields = ["idHorario"]
        extra_kwargs = {"duracionCita": {"min_value": 5}}

    def validate(self, attrs):
        inicio = _valor(self, attrs, "horaInicio")
        fin = _valor(self, attrs, "horaFin")
        if inicio and fin and fin <= inicio:
            raise serializers.ValidationError({"horaFin": "La hora de fin debe ser mayor que la de inicio."})
        return attrs


class ExcepcionHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcepcionHorario
        fields = ["idExcepcion", "doctor", "fecha", "todoElDia", "horaInicio", "horaFin", "motivo"]
        read_only_fields = ["idExcepcion"]

    def validate(self, attrs):
        todo_el_dia = _valor(self, attrs, "todoElDia")
        inicio = _valor(self, attrs, "horaInicio")
        fin = _valor(self, attrs, "horaFin")
        if todo_el_dia is False:
            if not inicio or not fin:
                raise serializers.ValidationError(
                    "Si la excepción no es de todo el día, indica horaInicio y horaFin."
                )
            if fin <= inicio:
                raise serializers.ValidationError({"horaFin": "La hora de fin debe ser mayor que la de inicio."})
        return attrs
