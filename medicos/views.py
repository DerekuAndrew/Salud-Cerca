from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from config.mixins import EliminacionProtegidaMixin, FiltrosQueryMixin
from .models import CentroMedico, Doctor, DoctorEspecialidad, Especialidad, ExcepcionHorario, Horario
from .serializers import (
    CentroMedicoSerializer, DoctorEspecialidadSerializer, DoctorSerializer,
    EspecialidadSerializer, ExcepcionHorarioSerializer, HorarioSerializer,
)


class CentroMedicoViewSet(EliminacionProtegidaMixin, FiltrosQueryMixin, viewsets.ModelViewSet):
    """CRUD de centros médicos. Filtros: ?ciudad= &activo="""

    queryset = CentroMedico.objects.all()
    serializer_class = CentroMedicoSerializer
    search_fields = ["nombre", "ciudad", "direccion"]
    ordering_fields = ["nombre", "ciudad"]
    filtros_query = {"ciudad": "ciudad__iexact", "activo": "activo"}


class EspecialidadViewSet(EliminacionProtegidaMixin, viewsets.ModelViewSet):
    """CRUD de especialidades médicas."""

    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    search_fields = ["nombre", "descripcion"]
    ordering_fields = ["nombre"]


class DoctorViewSet(EliminacionProtegidaMixin, FiltrosQueryMixin, viewsets.ModelViewSet):
    """CRUD de doctores. Filtros: ?centro= &especialidad= &activo="""

    queryset = Doctor.objects.select_related("centro", "usuario").prefetch_related("especialidades")
    serializer_class = DoctorSerializer
    search_fields = ["nombre", "apellido", "cedulaProfesional", "usuario__correo"]
    ordering_fields = ["apellido", "nombre"]
    filtros_query = {"centro": "centro_id", "especialidad": "especialidades", "activo": "activo"}

    @action(detail=True, methods=["get"])
    def horarios(self, request, pk=None):
        """GET /api/doctores/{id}/horarios/ -> horarios semanales del doctor."""
        doctor = self.get_object()
        datos = HorarioSerializer(doctor.horarios.all(), many=True).data
        return Response(datos)


class DoctorEspecialidadViewSet(EliminacionProtegidaMixin, FiltrosQueryMixin, viewsets.ModelViewSet):
    """Asigna especialidades a doctores. Filtros: ?doctor= &especialidad="""

    queryset = DoctorEspecialidad.objects.select_related("doctor", "especialidad")
    serializer_class = DoctorEspecialidadSerializer
    filtros_query = {"doctor": "doctor_id", "especialidad": "especialidad_id"}


class HorarioViewSet(EliminacionProtegidaMixin, FiltrosQueryMixin, viewsets.ModelViewSet):
    """Horarios semanales de los doctores. Filtros: ?doctor= &dia= (0=lunes ... 6=domingo)"""

    queryset = Horario.objects.select_related("doctor")
    serializer_class = HorarioSerializer
    ordering_fields = ["diaSemana", "horaInicio"]
    filtros_query = {"doctor": "doctor_id", "dia": "diaSemana"}


class ExcepcionHorarioViewSet(EliminacionProtegidaMixin, FiltrosQueryMixin, viewsets.ModelViewSet):
    """Días u horas en que un doctor no atiende. Filtros: ?doctor= &fecha=AAAA-MM-DD"""

    queryset = ExcepcionHorario.objects.select_related("doctor")
    serializer_class = ExcepcionHorarioSerializer
    search_fields = ["motivo"]
    ordering_fields = ["fecha"]
    filtros_query = {"doctor": "doctor_id", "fecha": "fecha"}
