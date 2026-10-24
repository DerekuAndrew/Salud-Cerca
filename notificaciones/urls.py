from rest_framework.routers import SimpleRouter

from .views import ConfiguracionViewSet, NotificacionViewSet

router = SimpleRouter()
router.register("notificaciones", NotificacionViewSet)
router.register("configuraciones", ConfiguracionViewSet)

urlpatterns = router.urls
