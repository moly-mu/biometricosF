from rest_framework import serializers
from .models import QRRecord

class RegistroQRSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRRecord
        fields = ['id', 'codigo_qr', 'estado', 'hora_entrada', 'hora_salida', 'tiempo_dentro']

class QRCodeSerializer(serializers.Serializer):
    nombres = serializers.CharField(max_length=255)
    apellidos = serializers.CharField(max_length=255)
    documento = serializers.CharField(max_length=50)