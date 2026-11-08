from rest_framework.viewsets import ModelViewSet
from encomiendas.models import GuiaEnvio, HistorialSeguimiento
from encomiendas.serializers import GuiaSerializer, HistorialSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated,IsAuthenticatedOrReadOnly
from encomiendas.models import ESTADOS_PAQUETE

#AllowAny permite cualquier peticion entrante
#IsAdminUser Solo administradores
#IsAuthenticated: Debe estar autenticado para acceder a el recurso
#IsAuthenticatedOrReadOnly: Este permiso permite que el usuario no este autenticado para las peticiones GET, pero el resto de peticiones HTTP si requiere estar autenticado


class GuiaViewSet(ModelViewSet):
    serializer_class = GuiaSerializer
    queryset = GuiaEnvio.objects.all()
    lookup_field = "numero_guia"
    permission_classes = [IsAuthenticatedOrReadOnly,]

    http_method_names = ["get", "post", "put", "delete"]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(creado_por=user)

    @action(detail=True, methods=['post'])
    def actualizar_estado(self, request, numero_guia=None):
        guia = self.get_object()
        estado = request.data.get('estado')
        observacion = request.data.get('observacion', '')
        usuario = request.user if request.user.is_authenticated else None

        if estado in dict(ESTADOS_PAQUETE):
            guia.estado_actual = estado
            guia.save()

            HistorialSeguimiento.objects.create(
                guia=guia,
                estado=estado,
                observacion=observacion,
                actualiado_por=usuario
            )
            return Response({'status': 'Estado actualizado correctamente'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Estado no válido'}, status=status.HTTP_400_BAD_REQUEST)

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

    