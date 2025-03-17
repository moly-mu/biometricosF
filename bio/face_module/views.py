from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cv2
import numpy as np
import base64
from .models import Usuario, RegistroAcceso, Asignatura
import face_recognition
import json
import subprocess
import requests
from datetime import datetime
from django.utils.timezone import now



def enviar_mensaje_whatsapp(numeros, mensaje):

    url = 'http://localhost:3000/enviar-mensaje'  # URL del endpoint del chatbot
    resultados = {}
    
    for numero in numeros:
        if numero:
            data = {
            'numero': numero,  # Número de teléfono del destinatario
            'mensaje': mensaje,  # Mensaje a enviar
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print(f"Mensaje enviado con éxito a {numero}.")
                resultados[numero] ="Enviado"
            else:
                print(f"Error al enviar mensaje a numero {numero}: {response.json()}")
                resultados[numero] = "Error"
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            resultados[numero] = "Error de conexión"
            
    return resultados    
        
def get_serial_number():
    try:
        output = subprocess.check_output(
            ['powershell', '-Command', '(Get-WmiObject win32_bios).SerialNumber'], 
            universal_newlines=True
        )
        return output.strip()
    except Exception as e:
        return f"Error: {e}"



    
class ReconocimientoFacialMixin:
    """
    Mixin con métodos comunes para el procesamiento de imágenes y reconocimiento facial.
    """
    def convertir_base64_a_imagen(self, imagen_base64):
        try:
            image_data = base64.b64decode(imagen_base64.split(",")[1])
            np_array = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            
            # Verificar que la imagen fue decodificada correctamente
            if img is None:
                print("Error: La imagen decodificada es None.")
                return None

            # Asegurar que la imagen es uint8
            if img.dtype != np.uint8:
                img = img.astype(np.uint8)

            # Asegurar que la imagen tiene exactamente 3 canales (RGB)
            if len(img.shape) == 3 and img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
            elif len(img.shape) == 2 or (len(img.shape) == 3 and img.shape[2] == 1):
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

            return img
        except Exception as e:
            print(f"Error al procesar la imagen Base64: {str(e)}")
            return None



    def comparar_rostros(self, rostro_nuevo, rostro_codificado_base):
        """
        Compara un rostro nuevo con un rostro almacenado.
        :param rostro_nuevo: Imagen recibida (en formato OpenCV).
        :param rostro_codificado_base: Codificación del rostro almacenado (serializada).
        :return: True si coinciden, False si no.
        """
        try:
            # Generar codificación facial para el rostro recibido
            codificaciones_nuevo = face_recognition.face_encodings(rostro_nuevo)
            if not codificaciones_nuevo:
                print("No se detectó un rostro en la imagen proporcionada.")
                return False

            # Convertir la codificación serializada a formato de lista
            rostro_codificado_base = json.loads(rostro_codificado_base)

            coincidencias = face_recognition.compare_faces([np.array(rostro_codificado_base)], codificaciones_nuevo[0], tolerance=0.5)
            return coincidencias[0]
        except Exception as e:
            print(f"Error al comparar rostros: {str(e)}")
            return False


class EntradaView(APIView, ReconocimientoFacialMixin):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({"status": "Error", "message": "Formato JSON inválido."}, status=status.HTTP_400_BAD_REQUEST)

        imagen_base64 = data.get("rostro_base64")
        if not imagen_base64:
            return Response({"status": "Error", "message": "Datos incompletos."}, status=status.HTTP_400_BAD_REQUEST)

        imagen_cv2 = self.convertir_base64_a_imagen(imagen_base64)
        if imagen_cv2 is None:
            return Response({"status": "Error", "message": "Imagen no válida."}, status=status.HTTP_400_BAD_REQUEST)

        numero_serie_entrada = get_serial_number()
        hora_actual = now()

        usuarios = Usuario.objects.all()
        for usuario in usuarios:
            if self.comparar_rostros(imagen_cv2, usuario.rostro_codificado):
                asignatura_actual = Asignatura.objects.filter(profesor=usuario, hora_inicio__lte=hora_actual, hora_fin__gte=hora_actual).first()
                
                if not asignatura_actual:
                    return Response({"status": "Error", "message": "No tiene clases en este horario."}, status=status.HTTP_400_BAD_REQUEST)

                # Registrar la entrada con la asignatura correspondiente
                RegistroAcceso.objects.create(
                    usuario=usuario,
                    estado="entrada",
                    hora_entrada=hora_actual,
                    numero_serie_entrada=numero_serie_entrada,
                    asignatura=asignatura_actual
                )

                mensaje_entrada = (f"Hola {usuario.nombre}, su entrada a la asignatura {asignatura_actual.nombre} "
                                   f"en la sede {asignatura_actual.sede} ha sido registrada a las {hora_actual.strftime('%H:%M:%S')}.")
                numeros_directivos = [usuario.whatsapp, usuario.directivo1, usuario.directivo2]
                enviar_mensaje_whatsapp(numeros_directivos, mensaje_entrada)

                return Response({"status": "Success", "message": "Entrada registrada"}, status=status.HTTP_201_CREATED)

        return Response({"status": "Error", "message": "Rostro no coincide."}, status=status.HTTP_400_BAD_REQUEST)


class SalidaView(APIView, ReconocimientoFacialMixin):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)  # Decodificar JSON si es necesario
        except json.JSONDecodeError:
            return Response({"status": "Error", "message": "Formato JSON inválido."}, status=status.HTTP_400_BAD_REQUEST)

        imagen_base64 = data.get("image_base64")
        if not imagen_base64:
            return Response({"status": "Error", "message": "Datos incompletos."}, status=status.HTTP_400_BAD_REQUEST)

        imagen_cv2 = self.convertir_base64_a_imagen(imagen_base64)
        if imagen_cv2 is None:
            return Response({"status": "Error", "message": "Imagen no válida."}, status=status.HTTP_400_BAD_REQUEST)

        hora_salida = now()
        numero_serie_salida = get_serial_number()

        usuarios = Usuario.objects.all()
        for usuario in usuarios:
            if self.comparar_rostros(imagen_cv2, usuario.rostro_codificado):
                ultimo_registro = RegistroAcceso.objects.filter(
                    usuario=usuario,
                    estado="entrada"
                ).order_by("-hora_entrada").first()

                if not ultimo_registro:
                    return Response({"status": "Error", "message": "No se encontró una entrada previa."}, status=status.HTTP_400_BAD_REQUEST)

                asignatura_actual = Asignatura.objects.filter(
                    profesor=usuario,
                    hora_inicio__lte=ultimo_registro.hora_entrada.time(),
                    hora_fin__gte=ultimo_registro.hora_entrada.time()
                ).first()
                
                if not asignatura_actual:
                    return Response({"status": "Error", "message": "No se encontró una asignatura para la entrada registrada."}, status=status.HTTP_400_BAD_REQUEST)

                tiempo_transcurrido = hora_salida - ultimo_registro.hora_entrada
                total_seconds = int(tiempo_transcurrido.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                tiempo_legible = f"{hours}h {minutes}m {seconds}s"

                # Crear un nuevo registro de salida
                RegistroAcceso.objects.create(
                    usuario=usuario,
                    hora_entrada=ultimo_registro.hora_entrada,
                    hora_salida=hora_salida,
                    tiempo_dentro=tiempo_transcurrido,
                    tiempo_legible=tiempo_legible,
                    estado="salida",
                    numero_serie_salida=numero_serie_salida,
                    asignatura=asignatura_actual
                )

                mensaje_salida = (f"Hola {usuario.nombre}, su salida de la asignatura {asignatura_actual.nombre} "
                                  f"en la sede {asignatura_actual.sede} ha sido registrada a las {hora_salida.strftime('%H:%M:%S')}. "
                                  f"Tiempo dentro: {tiempo_legible}.")

                numeros_directivos = [usuario.whatsapp, usuario.directivo1, usuario.directivo2]
                enviar_mensaje_whatsapp(numeros_directivos, mensaje_salida)

                return Response({"status": "Success", "message": "Salida registrada con éxito."}, status=status.HTTP_201_CREATED)

        return Response({"status": "Error", "message": "Rostro no coincide."}, status=status.HTTP_400_BAD_REQUEST)



class RegistrarRostroView(APIView, ReconocimientoFacialMixin):
    def post(self, request, *args, **kwargs):
        data = request.data
        nombre = data.get("nombre")
        cedula = data.get("cedula")
        whatsapp = data.get("whatsapp")
        imagen_base64 = data.get("image_base64")

        if not nombre or not cedula or not whatsapp or not imagen_base64:
            return Response({"status": "Error", "message": "Datos incompletos."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convertir imagen Base64 a formato OpenCV
            imagen_cv2 = self.convertir_base64_a_imagen(imagen_base64)
            if imagen_cv2 is not None:
                print(f"Imagen convertida correctamente: {imagen_cv2.shape}")
            else:
                print("Error: Imagen no válida después de convertir.")
                return Response({"status": "Error", "message": "Imagen no válida."}, status=status.HTTP_400_BAD_REQUEST)

            # Asegurarse de que la imagen esté en formato RGB o escala de grises
            if len(imagen_cv2.shape) == 3 and imagen_cv2.shape[2] in [3, 4]:
                if imagen_cv2.shape[2] == 4:
                    imagen_rgb = cv2.cvtColor(imagen_cv2, cv2.COLOR_BGRA2RGB)
                else:
                    imagen_rgb = imagen_cv2
            elif len(imagen_cv2.shape) == 2:  # Imagen en escala de grises
                imagen_rgb = cv2.cvtColor(imagen_cv2, cv2.COLOR_GRAY2RGB)
            else:
                print("Error: Formato de imagen no soportado. Forma de la imagen:", imagen_cv2.shape)
                return Response({"status": "Error", "message": "Formato de imagen no soportado."}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar si la imagen es uint8
            if imagen_rgb.dtype != np.uint8:
                imagen_rgb = imagen_rgb.astype(np.uint8)

            # Imprimir tipo de dato y canales para depuración
            print(f"Tipo de datos de imagen después de conversión: {imagen_rgb.dtype}, Forma: {imagen_rgb.shape}")
            
            # Redimensionar imagen a un tamaño estándar
            imagen_redimensionada = cv2.resize(imagen_rgb, (640, 480))
            print(f"Imagen redimensionada a: {imagen_redimensionada.shape}")
            
            # Verificar si hay un rostro en la imagen
            codificaciones = face_recognition.face_encodings(imagen_redimensionada)
            # Verificar si hay un rostro en la imagen
            codificaciones = face_recognition.face_encodings(imagen_rgb)
            if not codificaciones:
                print("Error: No se detectó un rostro válido en la imagen.")
                return Response({"status": "Error", "message": "No se detectó un rostro válido."}, status=status.HTTP_400_BAD_REQUEST)

            numero_serie = get_serial_number()

            usuario, created = Usuario.objects.update_or_create(
                cedula=cedula,
                defaults={
                    "nombre": nombre,
                    "whatsapp": whatsapp,
                    "numero_serie": numero_serie,
                    "rostro_base64": imagen_base64,
                    "rostro_codificado": json.dumps(codificaciones[0].tolist()),  # Serializar lista como JSON
                }
            )

            mensaje = "Usuario creado y rostro registrado." if created else "Rostro actualizado."
            return Response({"status": "Success", "message": mensaje}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"status": "Error", "message": f"Error interno: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

