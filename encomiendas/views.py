from rest_framework.viewsets import ModelViewSet
from encomiendas.models import GuiaEnvio, HistorialSeguimiento
from encomiendas.serializers import GuiaSerializer, HistorialSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated,IsAuthenticatedOrReadOnly

#AllowAny permite cualquier peticion entrante
#IsAdminUser Solo administradores
#IsAuthenticated: Debe estar autenticado para acceder a el recurso
#IsAuthenticatedOrReadOnly: Este permiso permite que el usuario no este autenticado para las peticiones GET, pero el resto de peticiones HTTP si requiere estar autenticado


class GuiaViewSet(ModelViewSet):
    serializer_class = GuiaSerializer
    queryset = GuiaEnvio.objects.all()
    lookup_field = "numero_guia"
    permission_classes = [IsAuthenticatedOrReadOnly,]

    #http_method_names = ["get", "post", "patch", "put", "delete"]

    #RE HACER METODO CREATE PARA TRAER PRECIO DEL BCV

    def get_queryset(self):
        queryset = GuiaEnvio.objects.all()

        estado = self.request.query_params.get('estado')

        if estado:
            queryset = queryset.filter(estado_actual__icontains=estado)

        return queryset

class HistorialViewSet(ModelViewSet):
    serializer_class = HistorialSerializer
    queryset = HistorialSeguimiento.objects.all()
    pagination_class = LimitOffsetPagination

    #http://127.0.0.1:8000/historial?limit=2&offset=2

    