from rest_framework import serializers
from encomiendas.models import GuiaEnvio, HistorialSeguimiento

class GuiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuiaEnvio
        fields = '__all__'

class HistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialSeguimiento
        fields = '__all__'