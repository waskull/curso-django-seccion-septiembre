from rest_framework import serializers
from cuentas.models import Perfil
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = "__all__"

class EmailLoginSerializer(TokenObtainPairSerializer):
    username_field = "email"
    def validate(self, datos):

        correo = datos.get("email")
        clave = datos.get("password")
        if correo and clave:
            usuario = authenticate(request=self.context.get("request"), email=correo, password=clave)

            if not usuario:
                raise serializers.ValidationError("Credenciales invalidas")
        else:
            raise serializers.ValidationError("Debes de proveer un correo y una clave")
        
        if not usuario.is_active:
            raise serializers.ValidationError("La cuenta fue deshabilitada")
        
        refresh_token = self.get_token(usuario)
        datos = {
            "access": str(refresh_token.access_token),
            "refresh": str(refresh_token)
        }
        return datos

