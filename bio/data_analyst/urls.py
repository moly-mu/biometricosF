from django.urls import path
from .views import generar_reporte_asistencia,reporte_general_csv 
from .viewsmongo import generar_reporte_asistencia_mongo

urlpatterns = [
    path('data/reporte_asistencia/',generar_reporte_asistencia, name='reporte_personal'),
    path('data/reporte_general_uno/',reporte_general_csv,name='reporte_general_bloque_uno'),
    path('data/basedatosvisual/',generar_reporte_asistencia_mongo, name='reporte_visual')
]
