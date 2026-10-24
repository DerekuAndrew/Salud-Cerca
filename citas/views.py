from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from config.mixins import EliminacionProtegidaMixin, FiltrosQueryMixin
from .models import Cita, Resena
from .serializers import CitaSerializer, ResenaSerializer


class CitaViewSet(EliminacionProtegidaMixin, FiltrosQueryMixin, viewsets.ModelViewSet):
    """CRUD de citas. Filtros: ?paciente= &doctor= &estado= &fecha=AAAA-MM-DD"""

    queryset = Cita.objects.select_related("paciente", "doctor", "especialidad")
    serializer_class = CitaSerializer
    search_fields = ["paciente__nombre", "paciente__apellido", "doctor__nombre", "doctor__apellido", "motivoConsulta"]
    ordering_fields = ["fechaCita", "horaInicio", "estado"]
    filtros_query = {
        "paciente": "paciente_id",
        "doctor": "doctor_id",
        "estado": "estado",
        "fecha": "fechaCita",
    }

    @action(detail=True, methods=["post"])
    def cancelar(self, request, pk=None):
        """POST /api/citas/{id}/cancelar/ -> cambia el estado a 'cancelada'."""
        cita = self.get_object()
        if cita.estado in (Cita.Estado.CANCELADA, Cita.Estado.COMPLETADA):
            return Response(
                {"detail": f"No se puede cancelar una cita {cita.get_estado_display().lower()}."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cita.estado = Cita.Estado.CANCELADA
        cita.save(update_fields=["estado", "fechaActualizacion"])
        return Response(self.get_serializer(cita).data)


class ResenaViewSet(EliminacionProtegidaMixin, FiltrosQueryMixin, viewsets.ModelViewSet):
    """CRUD de reseñas. Filtros: ?doctor= &paciente= &visible="""

    queryset = Resena.objects.select_related("cita", "paciente", "doctor")
    serializer_class = ResenaSerializer
    search_fields = ["comentario", "doctor__nombre", "doctor__apellido"]
    ordering_fields = ["fecha", "calificacion"]
    filtros_query = {"doctor": "doctor_id", "paciente": "paciente_id", "visible": "visible"}
