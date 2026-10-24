from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from config.mixins import EliminacionProtegidaMixin, FiltrosQueryMixin
from .models import Configuracion, Notificacion
from .serializers import ConfiguracionSerializer, NotificacionSerializer


class NotificacionViewSet(EliminacionProtegidaMixin, FiltrosQueryMixin, viewsets.ModelViewSet):
    """CRUD de notificaciones. Filtros: ?usuario= &leida= &tipo="""

    queryset = Notificacion.objects.select_related("usuario", "cita")
    serializer_class = NotificacionSerializer
    search_fields = ["titulo", "mensaje", "usuario__correo"]
    ordering_fields = ["fechaCreacion", "tipo"]
    filtros_query = {"usuario": "usuario_id", "leida": "leida", "tipo": "tipo"}

    @action(detail=True, methods=["post"], url_path="marcar-leida")
    def marcar_leida(self, request, pk=None):
        """POST /api/notificaciones/{id}/marcar-leida/ -> marca la notificación como leída."""
        notificacion = self.get_object()
        notificacion.leida = True
        notificacion.save(update_fields=["leida"])
        return Response(self.get_serializer(notificacion).data)


class ConfiguracionViewSet(EliminacionProtegidaMixin, viewsets.ModelViewSet):
    """CRUD de parámetros de configuración (clave-valor)."""

    queryset = Configuracion.objects.all()
    serializer_class = ConfiguracionSerializer
    search_fields = ["clave", "descripcion"]
    ordering_fields = ["clave"]
