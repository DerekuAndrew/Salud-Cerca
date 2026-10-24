from rest_framework import serializers

from .models import Configuracion, Notificacion


class NotificacionSerializer(serializers.ModelSerializer):
    usuario_correo = serializers.EmailField(source="usuario.correo", read_only=True)

    class Meta:
        model = Notificacion
        fields = [
            "idNotificacion", "usuario", "usuario_correo", "titulo", "mensaje",
            "tipo", "leida", "fechaCreacion", "cita",
        ]
        read_only_fields = ["idNotificacion", "fechaCreacion"]


class ConfiguracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracion
        fields = ["idConfig", "clave", "valor", "descripcion"]
        read_only_fields = ["idConfig"]
