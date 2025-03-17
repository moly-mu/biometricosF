from django.db import models
from django.utils.timezone import localtime


class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    cedula = models.CharField(max_length=50, unique=True)
    rostro_base64 = models.TextField(null=True, blank=True)  
    rostro_codificado = models.TextField(null=True, blank=True)
    whatsapp = models.CharField(max_length=15, null=True)
    directivo1 = models.CharField(max_length=12,default="573106135434")
    directivo2 = models.CharField(max_length=12,default="573134147100")  
    numero_serie = models.CharField(max_length=100, null=True)  

    def __str__(self):
        return self.nombre

class Asignatura(models.Model):
    nombre = models.CharField(max_length=255)
    profesor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    salon = models.CharField(max_length=50)
    sede = models.CharField(max_length=50)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

class RegistroAcceso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=10, default='entrada')
    hora_entrada = models.DateTimeField(max_length=100,null=True, blank=True)
    hora_salida = models.DateTimeField(max_length=100,null=True, blank=True)
    tiempo_dentro = models.DurationField(null=True, blank=True)
    hora_limite1 = models.TimeField(default="08:10:00")  # Hora de entrada primer bloque
    hora_limite2 = models.TimeField(default="10:10:00")
    tiempo_legible = models.CharField(max_length=50, null=True, blank=True)
    numero_serie_entrada = models.CharField(max_length=100, null=True)
    numero_serie_salida = models.CharField(max_length=100, null=True)

class Horario(models.Model):
    nombre = models.CharField(max_length=50)  # Ejemplo: "Bloque Uno", "Bloque Dos"
    hora_inicio = models.TimeField()
    hora_limite1 = models.TimeField()  # Límite para "a tiempo"
    hora_limite2 = models.TimeField()  # Límite para "tarde"
    hora_fin = models.TimeField()  # Fin del bloque

    def __str__(self):
        return self.nombre
    
    def get_fecha_local(self):
        return localtime(self.hora_entrada)
    
    
    def get_fecha_local(self):
        return localtime(self.hora_salida)

    def __str__(self):
        return f"{self.usuario.nombre if self.usuario else 'Sin usuario'} - {self.estado}"