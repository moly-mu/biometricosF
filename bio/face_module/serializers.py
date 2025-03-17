from rest_framework import serializers
from .models import Usuario, RegistroAcceso, Asignatura
from django.utils.timezone import localtime

class UsuarioSerializer(serializers.ModelSerializer):
    
    def get_fecha(self, obj):
        return localtime(obj.fecha).strftime('%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Usuario
        fields = "__all__"
        

class RegistroAccesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroAcceso
        fields = "__all__"


class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignatura
        fields = "__all__"
