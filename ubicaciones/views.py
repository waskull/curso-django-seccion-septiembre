from django.shortcuts import render
from ubicaciones.models import Agencia, Ciudad, Estado
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class EstadoView(APIView):
    def get(self, request):
        #print(self.request.method, self.request.data)
        data = [
            {
                "id": estado.pk,
                "nombre": estado.nombre
            } for estado in Estado.objects.all()
        ]

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        datos = self.request.data.copy()
        print(datos)
        existe = Estado.objects.filter(nombre__icontains=datos["nombre"]).exists()

        if existe:
            return Response({"mensaje":"Ese estado ya existe"}, status=status.HTTP_400_BAD_REQUEST)

        Estado.objects.create(**datos)

        return Response({"mensaje":f"El estado {datos["nombre"]} ha sido creado"}, status=status.HTTP_201_CREATED)

class EstadoViewDetail(APIView):
    def get(self, request, pk=None):
        #Primero valido si existe ese registro
        try:
            registro = Estado.objects.get(pk=pk)
        except Estado.DoesNotExist:
            return Response({"mensaje":"Ese estado no existe"}, status=status.HTTP_404_NOT_FOUND)
        registro = {
            "id": registro.id,
            "nombre": registro.nombre
        }

        return Response(registro, status=status.HTTP_200_OK)

