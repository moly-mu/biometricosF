from datetime import datetime, timedelta
from django.http import JsonResponse
from pymongo import MongoClient
from face_module.models import RegistroAcceso, Horario
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
mongo_db = client["asistencia"]
collection = mongo_db["asistencia_general"]

def generar_reporte_asistencia_mongo(request):
    fecha_fin = datetime.today().date()
    fecha_inicio = fecha_fin - timedelta(days=30)
    
    # Obtener todos los horarios de la base de datos
    horarios = Horario.objects.all()
    
    # Diccionario para almacenar los registros organizados por bloque horario
    reporte_mongo = []
    
    # Calcular el reporte para cada bloque horario
    for horario in horarios:
        registros = RegistroAcceso.objects.filter(
            hora_entrada__isnull=False,
            hora_entrada__date__gte=fecha_inicio,
            hora_entrada__time__gte=horario.hora_inicio,
            hora_entrada__time__lte=horario.hora_fin
        ).select_related("usuario")
        
        for registro in registros:
            estado = "A tiempo" if registro.hora_entrada and registro.hora_entrada.time() <= horario.hora_limite1 else "Tarde"
            
            registro_dict = {
                "bloque": horario.nombre,
                "nombre": registro.usuario.nombre if registro.usuario else "Sin nombre",
                "hora_entrada": registro.hora_entrada.strftime("%Y-%m-%d %H:%M:%S") if registro.hora_entrada else None,
                "numero_serie_entrada": registro.numero_serie_entrada if registro.numero_serie_entrada else None,
                "estado": estado,
                "fecha_reporte": datetime.utcnow()
            }
            
            reporte_mongo.append(registro_dict)
    
    # Insertar en MongoDB solo si hay datos nuevos
    if reporte_mongo:
        collection.insert_many(reporte_mongo)
        return JsonResponse({"mensaje": "Registros guardados en MongoDB exitosamente", "total_insertados": len(reporte_mongo)}, status=201)
    
    return JsonResponse({"mensaje": "No hay nuevos registros para insertar"}, status=200)
