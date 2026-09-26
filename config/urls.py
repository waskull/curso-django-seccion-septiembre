from django.contrib import admin
from django.urls import path, include
from ubicaciones.views import EstadoView, EstadoViewDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('estado/', name='estados', view=EstadoView.as_view()),
    path('estado/<int:pk>/', name="estado", view=EstadoViewDetail.as_view())
]
