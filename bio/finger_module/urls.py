from django.urls import path
from .views import EntradaHuellaView, SalidaHuellaView, RegistrarHuellaSecuGenView

urlpatterns = [
  path('EntradaHuella/', EntradaHuellaView.as_view(), name='estudiantesEntradaHuella'),
  path('SalidaHuella/', SalidaHuellaView.as_view(), name='estudiantesSalidaHuella'),
  path('RegistroHuella/', RegistrarHuellaSecuGenView.as_view(), name='estudiantesRegistroHuella'),
]
