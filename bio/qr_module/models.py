from django.db import models
from django.utils.timezone import make_aware
import pytz

class QRRecord(models.Model):
    qr_data = models.CharField(max_length=255, unique=True)  # Contenido del QR
    estado = models.CharField(max_length=20, choices=[("entrada", "Entrada"), ("salida", "Salida")])
    hora_entrada = models.DateTimeField(null=True, blank=True)
    hora_salida = models.DateTimeField(null=True, blank=True)
    tiempo_dentro = models.DurationField(null=True, blank=True)  # Tiempo total dentro
    tiempo_legible = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"{self.qr_data} - {self.estado}"

    def save(self, *args, **kwargs):
        # Zona horaria de Colombia
        colombia_tz = pytz.timezone('America/Bogota')

        # Si la hora de entrada no está definida, asignamos la hora actual con la zona horaria de Colombia
        if self.hora_entrada and self.hora_entrada.tzinfo is None:
            self.hora_entrada = make_aware(self.hora_entrada, timezone=colombia_tz)

        # Si la hora de salida no está definida, asignamos la hora actual con la zona horaria de Colombia
        if self.hora_salida and self.hora_salida.tzinfo is None:
            self.hora_salida = make_aware(self.hora_salida, timezone=colombia_tz)
            
        super(QRRecord, self).save(*args, **kwargs)

class QRCodeData(models.Model):
    nombres = models.CharField(max_length=100, default="Sin nombres")
    apellidos = models.CharField(max_length=100, default="Sin apellidos")
    documento = models.CharField(max_length=50, unique=True, default="0000000")
    qr_code_base64 = models.TextField()  # Para almacenar la imagen del QR en base64

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.documento}"
