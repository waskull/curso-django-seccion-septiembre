from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from cuentas.serializers import EmailLoginSerializer

class AuthView(TokenObtainPairView):
    serializer_class = EmailLoginSerializer

# Create your views here.
