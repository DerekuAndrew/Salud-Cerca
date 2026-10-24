from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from citas.urls import router as citas_router
from config.views import inicio
from medicos.urls import router as medicos_router
from notificaciones.urls import router as notificaciones_router
from usuarios.urls import router as usuarios_router

router = DefaultRouter()
for app_router in (usuarios_router, medicos_router, citas_router, notificaciones_router):
    router.registry.extend(app_router.registry)

urlpatterns = [
    path('', inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
