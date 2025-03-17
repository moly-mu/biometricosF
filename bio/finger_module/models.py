from django.db import models
from django.utils.timezone import now

class Estudiantes(models.Model):
    nombre = models.CharField(max_length=255)
    cedula = models.CharField(max_length=50, unique=True)
    rostro_base64 = models.TextField(null=True, blank=True)  # Imagen del rostro codificada en Base64
    rostro_codificado = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class RegistroAccesoHuella(models.Model):
    # Hacer usuario anulable temporalmente
    usuario = models.ForeignKey(Estudiantes, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=10, default='entrada')
    hora_entrada = models.DateTimeField(null=True, blank=True)
    hora_salida = models.DateTimeField(null=True, blank=True)
    tiempo_dentro = models.DurationField(null=True, blank=True)
    tiempo_legible = models.CharField(max_length=50, null=True, blank=True) 

    def __str__(self):
        return f"{self.usuario.nombre if self.usuario else 'Sin usuario'} - {self.estado}"
