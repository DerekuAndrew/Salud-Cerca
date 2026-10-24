from rest_framework.routers import SimpleRouter

from .views import (
    CentroMedicoViewSet, DoctorEspecialidadViewSet, DoctorViewSet,
    EspecialidadViewSet, ExcepcionHorarioViewSet, HorarioViewSet,
)

router = SimpleRouter()
router.register("centros", CentroMedicoViewSet)
router.register("especialidades", EspecialidadViewSet)
router.register("doctores", DoctorViewSet)
router.register("doctor-especialidades", DoctorEspecialidadViewSet)
router.register("horarios", HorarioViewSet)
router.register("excepciones-horario", ExcepcionHorarioViewSet)

urlpatterns = router.urls
