from django.contrib import admin
from django.urls import path, include
from ubicaciones.views import CiudadViewSet, EstadoView, EstadoViewDetail
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'ciudad', basename="ciudades", viewset=CiudadViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('estado/', name='estados', view=EstadoView.as_view()),
    path('estado/<int:pk>/', name="estado", view=EstadoViewDetail.as_view()),
    path('', include(router.urls))
]
