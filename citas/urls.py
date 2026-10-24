from rest_framework.routers import SimpleRouter

from .views import CitaViewSet, ResenaViewSet

router = SimpleRouter()
router.register("citas", CitaViewSet)
router.register("resenas", ResenaViewSet)

urlpatterns = router.urls
