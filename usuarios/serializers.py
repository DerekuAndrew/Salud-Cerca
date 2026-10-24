from django.contrib.auth import password_validation
from django.utils import timezone
from rest_framework import serializers

from .models import Paciente, Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    # La contraseña solo se escribe; nunca se devuelve en las respuestas.
    password = serializers.CharField(
        write_only=True, required=False, style={"input_type": "password"},
        help_text="Obligatoria al crear. Al editar, solo se cambia si se envía.",
    )

    class Meta:
        model = Usuario
        fields = ["idUsuario", "correo", "password", "rol", "activo", "fechaRegistro", "last_login"]
        read_only_fields = ["idUsuario", "fechaRegistro", "last_login"]

    def validate_password(self, valor):
        password_validation.validate_password(valor)
        return valor

    def validate(self, attrs):
        if self.instance is None and not attrs.get("password"):
            raise serializers.ValidationError({"password": "Este campo es obligatorio."})
        return attrs

    def create(self, validated_data):
        # create_user cifra la contraseña con set_password (hash).
        password = validated_data.pop("password")
        return Usuario.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        usuario = super().update(instance, validated_data)
        if password:
            usuario.set_password(password)
            usuario.save()
        return usuario


class PacienteSerializer(serializers.ModelSerializer):
    correo = serializers.EmailField(source="usuario.correo", read_only=True)

    class Meta:
        model = Paciente
        fields = [
            "idPaciente", "usuario", "correo", "nombre", "apellido",
            "telefono", "fechaNacimiento", "genero", "direccion",
        ]
        read_only_fields = ["idPaciente"]

    def validate_usuario(self, usuario):
        if usuario.rol != Usuario.Rol.PACIENTE:
            raise serializers.ValidationError("El usuario debe tener el rol 'paciente'.")
        return usuario

    def validate_fechaNacimiento(self, valor):
        if valor and valor > timezone.localdate():
            raise serializers.ValidationError("La fecha de nacimiento no puede ser futura.")
        return valor
