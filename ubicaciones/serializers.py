from rest_framework import serializers
from ubicaciones.models import Agencia, Estado, Ciudad
from uuid import uuid4

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = '__all__'

class CiudadGETSerializer(serializers.ModelSerializer):
    estado_nombre = serializers.ReadOnlyField(source='estado.nombre')
    class Meta:
        model = Ciudad
        fields = '__all__'

class AgenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agencia
        fields = '__all__'

    def validate(self, data):
        if str(data["rif"]).startswith('V') or str(data["rif"]).startswith('J'):
            print("todo bien")
        else: 
            raise serializers.ValidationError("el formato enviado no coincide con lo requerido") 

        return data

    def to_internal_value(self, data):

        datos = data.copy()

        if "codigo" not in datos or not datos["datos"]:
            datos["codigo"] = uuid4().hex

        return super().to_internal_value(datos)