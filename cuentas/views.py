from rest_framework_simplejwt.views import TokenObtainPairView
from cuentas.serializers import EmailLoginSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated,IsAuthenticatedOrReadOnly
from cuentas.serializers import UsuarioSerializer
from django.contrib.auth.models import User

class AuthView(TokenObtainPairView):
    serializer_class = EmailLoginSerializer

# Create your views here.
class UsuarioViewSet(ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = User.objects.select_related('perfil').all()
    permission_classes = [IsAuthenticatedOrReadOnly,]
    http_method_names = ["get", "post", "put", "delete"]

                                        #url_path sirve para personalizar el nombre de la nueva ruta
    @action(detail=False, methods=["GET"], url_path="perfil", permission_classes=[IsAuthenticatedOrReadOnly,])
    def perfil(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)