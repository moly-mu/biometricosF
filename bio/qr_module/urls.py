from django.urls import path
from .views import QREntradaView, QRSalidaView, QRCodeAPI, descargar_qr

urlpatterns = [
     path('qr_scanner_entrada/', QREntradaView.as_view(), name='qr_entrada'),
     path('qr_scanner_salida/', QRSalidaView.as_view(), name='qr_salida'),
     path('api/generar-qr/', QRCodeAPI.as_view(), name='generar_qr'),
     path('qr/descargas/<str:filename>/', descargar_qr, name='descargar_qr'),
]
