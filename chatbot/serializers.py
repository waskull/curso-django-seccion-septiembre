from rest_framework.serializers import ModelSerializer
from chatbot.models import Conversacion

class ConversacionSerializer(ModelSerializer):
    class Meta:
        model = Conversacion
        fields = ('pregunta','respuesta','modelo','temperatura','usuario')
        read_only_fields=('usuario','respuesta')