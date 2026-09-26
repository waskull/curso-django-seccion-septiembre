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
        try:
            registro = Estado.objects.get(pk=pk)
        except Estado.DoesNotExist:
            return Response({"mensaje":"Ese estado no existe"}, status=status.HTTP_404_NOT_FOUND)
        registro = {
            "id": registro.id,
            "nombre": registro.nombre
        }

        return Response(registro, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
            try:
                registro = Estado.objects.get(pk=pk)
                registro.delete()
            except Estado.DoesNotExist:
                return Response({"mensaje":"Ese estado no existe"}, status=status.HTTP_404_NOT_FOUND)
    
            return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk=None):
        nombre = self.request.data["nombre"]
        if not nombre:
            return Response({"mensaje":"El nombre es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            registro = Estado.objects.get(pk=pk)
            registro.nombre = nombre
            registro.save()
        except Estado.DoesNotExist:
            return Response({"mensaje":"Ese estado no existe"}, status=status.HTTP_404_NOT_FOUND)


        return Response({"mensaje":"El registro se ha editado"}, status=status.HTTP_200_OK)

    def patch(self,request,pk=None):
        return self.put(request=request,pk=pk)


from rest_framework.viewsets import ViewSet

class CiudadViewSet(ViewSet):
    def list(self, request):
        data = [
            {
                "id": ciudad.pk,
                "nombre": ciudad.nombre,
                "estado": ciudad.estado.nombre
            } for ciudad in Ciudad.objects.all()
        ]

        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
            try:
                registro = Ciudad.objects.get(pk=pk)
            except Ciudad.DoesNotExist:
                return Response({"mensaje":"Esa ciudad no existe"}, status=status.HTTP_404_NOT_FOUND)
            registro = {
                "id": registro.id,
                "nombre": registro.nombre,
                "estado":registro.estado.nombre
            }
    
            return Response(registro, status=status.HTTP_200_OK)

    def create(self, request): #post para crear registros
        datos = self.request.data.copy()
        id_estado = datos["estado"]
        estado = Estado.objects.get(id=id_estado)
        existe = Ciudad.objects.filter(nombre__icontains=datos["nombre"], estado=estado).exists()

        if existe:
            return Response({"mensaje":f"{datos["nombre"]} ya existe registrada en el estado {estado.nombre}"}, status=status.HTTP_400_BAD_REQUEST)

        Ciudad.objects.create(estado=estado,nombre=datos["nombre"])

        return Response({"mensaje":f"La ciudad {datos["nombre"]} ha sido creada"}, status=status.HTTP_201_CREATED)

    def update(self,request,pk=None): #metodo http para editar todo un recurso. put
        pass
    def partial_update(self,request,pk=None): #metodo para editar un recurso parcialmente, patch
        pass
    def delete(self,request,pk=None): #delete
        ...