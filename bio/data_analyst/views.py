import csv
import pandas as pd
from face_module.models import RegistroAcceso, Horario
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from django.db.models import Count,Q,F
from django.http import JsonResponse
from face_module.models import RegistroAcceso

def reporte_general_csv(request):
    # Obtener todos los horarios de la base de datos
    horarios = Horario.objects.all()

    # Crear un diccionario para almacenar los resultados
    reporte = {}

    # Calcular el reporte para cada bloque horario
    for horario in horarios:
        reporte[horario.nombre] = RegistroAcceso.objects.aggregate(
            a_tiempo=Count('id', filter=Q(hora_entrada__isnull=False, 
                                          hora_entrada__time__lte=horario.hora_limite1,
                                          hora_entrada__time__gte=horario.hora_inicio)),
            tarde=Count('id', filter=Q(hora_entrada__isnull=False, 
                                       hora_entrada__time__gt=horario.hora_limite1,
                                       hora_entrada__time__lte=horario.hora_limite2)),
            fuera_de_horario=Count('id', filter=Q(hora_entrada__isnull=False, 
                                                  hora_entrada__time__gt=horario.hora_limite2,
                                                  hora_entrada__time__lte=horario.hora_fin))
        )

    # Crear la respuesta HTTP con contenido CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_general.csv"'

    # Crear el escritor CSV
    writer = csv.writer(response)
    
    # Escribir la cabecera del CSV
    writer.writerow(["Bloque", "A Tiempo", "Tarde", "Fuera de Horario"])

    # Escribir los datos de cada bloque en el CSV
    for nombre_bloque, datos in reporte.items():
        writer.writerow([nombre_bloque, datos["a_tiempo"], datos["tarde"], datos["fuera_de_horario"]])

    return response

def generar_reporte_asistencia(request):
    # Obtener todos los horarios de la base de datos
    horarios = Horario.objects.all()

    # Crear un diccionario para almacenar los resultados
    reporte = {}

    # Calcular el reporte para cada bloque horario
    for horario in horarios:
        registros = RegistroAcceso.objects.filter(
            hora_entrada__isnull=False,
            hora_entrada__time__gte=horario.hora_inicio,
            hora_entrada__time__lte=horario.hora_fin
        ).select_related("usuario")
        
        # Construir datos con formato específico para entrada
        reporte[horario.nombre] = [
            {
                "nombre": registro.usuario.nombre if registro.usuario else "Sin nombre",
                "hora_entrada": registro.hora_entrada.strftime("%Y-%m-%d %H:%M:%S") if registro.hora_entrada else "",
                "numero_serie_entrada": registro.numero_serie_entrada if registro.numero_serie_entrada else "",
                "estado": "A tiempo" if registro.hora_entrada and registro.hora_entrada.time() <= horario.hora_limite1 else "Tarde"
            }
            for registro in registros
        ]
    
    # Crear la respuesta HTTP con contenido CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_general.csv"'

    # Crear el escritor CSV
    writer = csv.writer(response)
    
    # Escribir la cabecera del CSV
    writer.writerow(["Bloque", "Nombre", "Hora Entrada", "Número Serie Entrada", "Estado"])
    
    # Escribir los datos de cada bloque en el CSV
    for nombre_bloque, datos in reporte.items():
        for registro in datos:
            writer.writerow([nombre_bloque, registro["nombre"], registro["hora_entrada"], registro["numero_serie_entrada"], registro["estado"]])
    
    return response