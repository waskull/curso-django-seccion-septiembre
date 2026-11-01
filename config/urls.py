from django.contrib import admin
from django.urls import path, include
from encomiendas.views import GuiaViewSet, HistorialViewSet
from ubicaciones.views import CiudadViewSet, EstadoView, EstadoViewDetail, AgenciaViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from cuentas.views import AuthView

router = DefaultRouter()
router.register(r'ciudad', basename="ciudades", viewset=CiudadViewSet)
router.register(r'agencia', basename='agencias', viewset=AgenciaViewSet)
router.register(r'guia', basename='guias', viewset=GuiaViewSet)
router.register(r'historial', basename='historiales', viewset=HistorialViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('estado/', name='estados', view=EstadoView.as_view()),
    path('estado/<int:pk>/', name="estado", view=EstadoViewDetail.as_view()),
    path('auth/login/', name="login",view=AuthView.as_view()),
    path('auth/refresh/', name="refresh_token", view=TokenRefreshView.as_view()),
    path('', include(router.urls))
]
