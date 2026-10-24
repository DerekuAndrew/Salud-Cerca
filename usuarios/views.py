from rest_framework import viewsets

from config.mixins import EliminacionProtegidaMixin
from .models import Paciente, Usuario
from .serializers import PacienteSerializer, UsuarioSerializer


class UsuarioViewSet(EliminacionProtegidaMixin, viewsets.ModelViewSet):
    """CRUD de usuarios (cuentas de acceso)."""

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    search_fields = ["correo"]
    ordering_fields = ["correo", "fechaRegistro", "rol"]


class PacienteViewSet(EliminacionProtegidaMixin, viewsets.ModelViewSet):
    """CRUD de pacientes."""

    queryset = Paciente.objects.select_related("usuario")
    serializer_class = PacienteSerializer
    search_fields = ["nombre", "apellido", "telefono", "usuario__correo"]
    ordering_fields = ["apellido", "nombre", "fechaNacimiento"]
