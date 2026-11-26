from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from chatbot.models import Conversacion
from chatbot.serializers import ConversacionSerializer
from chatbot.rag import generar_respuesta, generar_respuesta_google
from ubicaciones.models import Agencia
from encomiendas.models import GuiaEnvio

class ChatbotView(APIView):
    serializer_class = ConversacionSerializer

    def get(self,request):
        datos = Conversacion.objects.filter(usuario=self.request.user)
        serializer = ConversacionSerializer(datos, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        engine = self.request.query_params.get('engine', "openrouter").lower()
        modelo = serializer.validated_data.get("modelo", "openai/gpt-oss-120b")
        pregunta = serializer.validated_data["pregunta"].lower()

        if engine == "groq" and modelo not in ('openai/gpt-oss-120b','openai/gpt-oss-20b','qwen/qwen3.8-27b'):
            return Response({"error":"El modelo seleccionado no esta disponible para groq"},status=status.HTTP_400_BAD_REQUEST)
        
        if engine == "google" and modelo not in ('gemma-4-26b-a4b-it','gemma-4-31b-it','gemini-3.5-flash-lite','gemini-3.8-flash','gemini-3.6-flash'):
            return Response({"error":"El modelo seleccionado no esta disponible para Google AI Studio"},status=status.HTTP_400_BAD_REQUEST)
        
        agencias = Agencia.objects.all()
        guias = GuiaEnvio.objects.all()
        historiales = Conversacion.objects.filter(usuario=self.request.user)[:4]
        historial = "\n".join(
            [f"Pregunta: {h.pregunta.lower()} - Respuesta: {h.respuesta.lower()}" for h in historiales]
        ) 
        contexto = "\n".join(
            [f"Paquete: {p.numero_guia} | Remitente: {p.remitente} | Destinatario: {p.destinatario} | Peso: {p.peso_kg} | Estado: {p.estado_actual.lower()}" for p in guias])
        
        lista_agencias = "\n".join(
                    [f"Agencia: {p.nombre} | Ciudad: {p.ciudad} | Direccion: {p.direccion}" for p in agencias])
        if lista_agencias: contexto+=f"\n {lista_agencias}"
        if historial == None or historial == "":
            historial = "SIN HISTORIAL RELEVANTE"
        SYSTEM_PROMPT = (
            "Eres el asistente del sistema de envio de paquetes llamado RapiEnvios. "
            "Usa solo la información provista en el 'CONTEXT' para responder "
            "consultas sobre el estado del paquete. "
            "Si no puedes responder con la información disponible, indica que no puedes responder."
        )
        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"=== CONTEXT ===\n{contexto}\n\n"
            f"=== HISTORIAL PREVIO === \n {historial}\n"
            "=== INSTRUCCIÓN ===\n"
            "Responde solo con información del contexto. Sé claro, conciso y emite la respuesta en texto plano.\n"
        )

        temperatura = serializer.validated_data.get("temperatura", 0.8)
        try:
            print("Haciendo petición a Llama.cpp con el modelo:", modelo)
            print("Prompt:", prompt)
            print("Pregunta:", pregunta)
            print("Engine:", engine)
            if engine != "google": respuesta = generar_respuesta(prompt,pregunta, temperatura=temperatura,modelo=modelo, engine=engine)
            else: respuesta = generar_respuesta_google(prompt,pregunta, temperatura=temperatura,modelo=modelo)

            print("Respuesta:", respuesta)
            LISTA_ERROR = ["No puedo responder a esa pregunta.",
                           "No puedo responder a tu pregunta.", "No puedo responder a tu pregunta", ""]
            if respuesta or respuesta not in LISTA_ERROR:
               Conversacion.objects.create(respuesta=respuesta,pregunta=pregunta,modelo=modelo,usuario=self.request.user,temperatura=temperatura)
               return Response({"pregunta": pregunta, "respuesta": respuesta})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        return Response({"mensaje":"Un error desconocido ha ocurrido"}, status=status.HTTP_400_BAD_REQUEST)