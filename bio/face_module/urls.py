from django.urls import path
from .views import EntradaView, SalidaView, RegistrarRostroView

urlpatterns = [
    path('facial/entrada/', EntradaView.as_view(), name='entrada'),
    path('facial/salida/', SalidaView.as_view(), name='salida'),
    path('facial/registrarRostros/', RegistrarRostroView.as_view(), name='salida'),
]