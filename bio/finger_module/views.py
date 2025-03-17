from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Estudiantes, RegistroAccesoHuella
from django.utils.timezone import now
import json
import ctypes
import base64

# Cambiar ruta a donde está el archivo dll del sistema operativo
#sg_fpm = ctypes.CDLL(r'D:\GrabacionDavid\FDx SDK Pro for Windows v4.3.1_J1.12\FDx SDK Pro for Windows v4.3.1\DotNETFramework\Bin\x64\SecuGen.FDxSDKPro.Windows.dll')

class SGFingerPrintManager:
    def __init__(self):
        # Asumiendo que el SDK tiene una función de inicialización
        #self.fp_manager = sg_fpm.SGFPM_Initialize  # Asegúrate de que esta función exista en la DLL

    #def GetImage(self):
        """Captura la imagen de la huella digital."""
        # El SDK de SecuGen tendrá funciones que devuelven imágenes de huellas
        return self.fp_manager()  # Modifica esto según las funciones disponibles

    def SetTemplateFormat(self, format):
        """Configura el formato del template para comparación."""
        # Configuración del formato, puedes adaptar según las funciones disponibles en la DLL
        self.fp_manager.SGFPM_SetTemplateFormat(format)

    def MatchTemplate(self, huella_capturada, huella_codificada_base):
        """Compara las huellas dactilares."""
        # Llamada a la función para comparar las huellas en el SDK
        result = self.fp_manager.SGFPM_MatchTemplate(huella_capturada, huella_codificada_base)
        return result  # Aquí deberás manejar el valor de retorno según lo definido en la DLL

    def GetError(self):
        """Obtiene el error o mensaje de la última operación."""
        # Función de error en el SDK de SecuGen
        return self.fp_manager.SGFPM_GetError()


class ReconocimientoHuellaSecuGenMixin:
    def __init__(self):
        self.fp_manager = SGFingerPrintManager()

    def capturar_huella(self):
        try:
            result = self.fp_manager.GetImage()  # Captura la imagen de la huella
            if result[0] == 0:  # 0 indica éxito en la captura
                return result[1]  # Devuelve la imagen de la huella
            else:
                print(f"Error al capturar huella: {self.fp_manager.GetError()}")
                return None
        except Exception as e:
            print(f"Error durante la captura de la huella: {str(e)}")
            return None

    def comparar_huellas(self, huella_capturada, huella_codificada_base):
        try:
            self.fp_manager.SetTemplateFormat(1)  # Configura el formato del template
            result = self.fp_manager.MatchTemplate(huella_capturada, json.loads(huella_codificada_base))
            return result[0] == 0  # 0 indica coincidencia
        except Exception as e:
            print(f"Error al comparar huellas: {str(e)}")
            return False

class EntradaHuellaView(APIView, ReconocimientoHuellaSecuGenMixin):
    def post(self, request, *args, **kwargs):
        try:
            huella_capturada = self.capturar_huella()

            if huella_capturada is None:
                return Response({"status": "Error", "message": "Error al capturar la huella."}, status=status.HTTP_400_BAD_REQUEST)

            usuarios = Estudiantes.objects.all()
            for usuario in usuarios:
                if self.comparar_huellas(huella_capturada, usuario.huella_codificada):
                    registro, created = RegistroAccesoHuella.objects.get_or_create(usuario=usuario, estado="entrada")
                    if created or registro.estado == "salida":
                        registro.estado = "entrada"
                        registro.hora_entrada = now()
                        registro.hora_salida = None
                        registro.tiempo_dentro = None
                        registro.save()
                        return Response({"status": "Success", "message": "Entrada registrada."}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"status": "Complete", "message": "Ya se ha registrado como entrada."}, status=status.HTTP_200_OK)

            return Response({"status": "Error", "message": "Huella no coincide."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"status": "Error", "message": f"Error interno del servidor: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SalidaHuellaView(APIView, ReconocimientoHuellaSecuGenMixin):
    def post(self, request, *args, **kwargs):
        try:
            huella_capturada = self.capturar_huella()

            if huella_capturada is None:
                return Response({"status": "Error", "message": "Error al capturar la huella."}, status=status.HTTP_400_BAD_REQUEST)

            usuarios = Estudiantes.objects.all()
            for usuario in usuarios:
                if self.comparar_huellas(huella_capturada, usuario.huella_codificada):
                    registro = RegistroAccesoHuella.objects.filter(usuario=usuario, estado="entrada").last()

                    if registro and registro.estado == "entrada":
                        registro.estado = "salida"
                        registro.hora_salida = now()
                        tiempo_transcurrido = registro.hora_salida - registro.hora_entrada

                        total_seconds = int(tiempo_transcurrido.total_seconds())
                        hours, remainder = divmod(total_seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        tiempo_legible = f"{hours}h {minutes}m {seconds}s"

                        registro.tiempo_dentro = tiempo_transcurrido
                        registro.tiempo_legible = tiempo_legible
                        registro.save()

                        return Response({"status": "Success", "message": "Salida registrada."}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"status": "Error", "message": "No se encontró una entrada previa."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"status": "Error", "message": "Huella no coincide."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"status": "Error", "message": f"Error interno del servidor: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegistrarHuellaSecuGenView(APIView, ReconocimientoHuellaSecuGenMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Llama al constructor de la clase base
        ReconocimientoHuellaSecuGenMixin.__init__(self)  # Asegura que el constructor de la mezcla también se llame

    def post(self, request, *args, **kwargs):
        data = request.data
        nombre = data.get("nombre")
        cedula = data.get("cedula")

        if not nombre or not cedula:
            return Response({"status": "Error", "message": "Datos incompletos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            huella_capturada = self.capturar_huella()

            if huella_capturada is None:
                return Response({"status": "Error", "message": "Error al capturar la huella."}, status=status.HTTP_400_BAD_REQUEST)

            usuario, created = Estudiantes.objects.update_or_create(
                cedula=cedula,
                defaults={
                    "nombre": nombre,
                    "huella_base64": base64.b64encode(huella_capturada).decode('utf-8'),
                    "huella_codificada": json.dumps(huella_capturada.tolist()),
                }
            )

            mensaje = "Usuario creado y huella registrada." if created else "Huella actualizada."
            return Response({"status": "Success", "message": mensaje}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"status": "Error", "message": f"Error interno: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
