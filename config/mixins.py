"""Piezas reutilizables para todas las vistas de la API."""
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.response import Response


class EliminacionProtegidaMixin:
    """Evita el error 500 cuando se borra un registro del que otros dependen
    (por ejemplo, un doctor que ya tiene citas). Responde 409 con un mensaje."""

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": "No se puede eliminar este registro porque otros registros dependen de él."},
                status=status.HTTP_409_CONFLICT,
            )


class FiltrosQueryMixin:
    """Filtra el listado con parámetros de la URL.

    Ejemplo: filtros_query = {"doctor": "doctor_id"} permite GET /api/citas/?doctor=3
    """

    filtros_query = {}

    def get_queryset(self):
        queryset = super().get_queryset()
        for parametro, campo in self.filtros_query.items():
            valor = self.request.query_params.get(parametro)
            if valor in (None, ""):
                continue
            if valor.lower() in ("true", "false"):
                valor = valor.lower() == "true"
            try:
                queryset = queryset.filter(**{campo: valor})
            except (ValueError, TypeError, DjangoValidationError):
                # Valor inválido (por ejemplo ?doctor=abc): devolvemos lista vacía.
                return queryset.none()
        return queryset
