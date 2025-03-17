from rest_framework import serializers
from .models import Estudiantes, RegistroAccesoHuella

class EstudiantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiantes
        fields = ['id', 'nombre', 'cedula', 'rostro_base64', 'rostro_codificado']
        read_only_fields = ['id']  # Puedes hacer que el campo id sea solo lectura

class RegistroAccesoHuellaSerializer(serializers.ModelSerializer):
    usuario = EstudiantesSerializer(read_only=True)  # Si no quieres que el usuario se pueda modificar a través del serializer

    class Meta:
        model = RegistroAccesoHuella
        fields = ['id', 'usuario', 'estado', 'hora_entrada', 'hora_salida', 'tiempo_dentro', 'tiempo_legible']
        read_only_fields = ['id', 'usuario']  # Hacemos que el usuario sea solo lectura, ya que no lo queremos modificar directamente
