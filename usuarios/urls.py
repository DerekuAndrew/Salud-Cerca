from rest_framework.routers import SimpleRouter

from .views import PacienteViewSet, UsuarioViewSet

router = SimpleRouter()
router.register("usuarios", UsuarioViewSet)
router.register("pacientes", PacienteViewSet)

urlpatterns = router.urls
