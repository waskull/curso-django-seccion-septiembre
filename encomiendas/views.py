from rest_framework.viewsets import ModelViewSet
from encomiendas.models import GuiaEnvio, HistorialSeguimiento
from encomiendas.serializers import GuiaSerializer, HistorialSerializer

class GuiaViewSet(ModelViewSet):
    serializer_class = GuiaSerializer
    queryset = GuiaEnvio.objects.all()
    lookup_field = "numero_guia"

    def get_queryset(self):
        queryset = GuiaEnvio.objects.all()

        estado = self.request.query_params.get('estado')

        if estado:
            queryset = queryset.filter(estado_actual__icontains=estado)

        return queryset

class HistorialViewSet(ModelViewSet):
    serializer_class = HistorialSerializer
    queryset = HistorialSeguimiento.objects.all()

    