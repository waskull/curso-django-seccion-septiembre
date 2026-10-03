from rest_framework.viewsets import ModelViewSet
from encomiendas.models import GuiaEnvio, HistorialSeguimiento
from encomiendas.serializers import GuiaSerializer, HistorialSerializer

class GuiaViewSet(ModelViewSet):
    serializer_class = GuiaSerializer
    queryset = GuiaEnvio.objects.all()

    lookup_field = "numero_guia"

class HistorialViewSet(ModelViewSet):
    serializer_class = HistorialSerializer
    queryset = HistorialSeguimiento.objects.all()