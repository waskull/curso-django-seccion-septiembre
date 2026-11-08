from decimal import Decimal
from utils.bcv import obtener_dolar_bcv_manual
from rest_framework import serializers
from encomiendas.models import GuiaEnvio, HistorialSeguimiento

class GuiaSerializer(serializers.ModelSerializer):
    monto_usd = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, allow_null=True)
    monto_bolivares = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)

    def create(self, validated_data):
        monto_usd = validated_data.get('monto_usd')
        monto_bolivares = validated_data.get('monto_bolivares')
        tasa_bcv = obtener_dolar_bcv_manual()

        if monto_usd and tasa_bcv:
            if not monto_bolivares:
                validated_data['monto_bolivares'] = Decimal(str(monto_usd)) * Decimal(str(tasa_bcv))
        elif monto_bolivares and tasa_bcv and not monto_usd:
            validated_data['monto_usd'] = Decimal(str(monto_bolivares)) / Decimal(str(tasa_bcv))

        return super().create(validated_data)

    class Meta:
        model = GuiaEnvio
        fields = '__all__'
        read_only_fields = ['numero_guia', 'estado_actual', 'fecha_creacion', 'creado_por']

class HistorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialSeguimiento
        fields = '__all__'