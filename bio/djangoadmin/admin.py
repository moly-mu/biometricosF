from django.contrib import admin
from face_module.models import Usuario, RegistroAcceso, Asignatura

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'whatsapp', 'numero_serie')
    search_fields = ('nombre', 'cedula')
    list_filter = ('numero_serie',)

@admin.register(RegistroAcceso)
class RegistroAccesoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'estado', 'hora_entrada', 'hora_salida', 'tiempo_legible','numero_serie_entrada','numero_serie_salida')
    search_fields = ('usuario__nombre', 'numero_serie_entrada', 'numero_serie_salida')
    list_filter = ('estado',)

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "profesor", "salon", "sede", "hora_inicio", "hora_fin")
    search_fields = ("nombre", "profesor__nombre", "sede", "salon")
    list_filter = ("sede", "hora_inicio", "hora_fin")