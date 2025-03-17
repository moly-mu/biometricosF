from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pyzbar.pyzbar import decode
import cv2
import base64
import numpy as np
from django.utils.timezone import now
from .models import QRRecord
from .models import QRCodeData
from .serializers import QRCodeSerializer
import qrcode
from io import BytesIO
from django.http import HttpResponse

class QREntradaView(APIView):
    """
    Procesa la entrada de un QR.
    """
    def convertir_imagen_a_base64(self, imagen_cv2):
        try:
            success, buffer = cv2.imencode('.png', imagen_cv2)
            if not success:
                raise ValueError("No se pudo codificar la imagen a formato PNG")
            return f"data:image/png;base64,{base64.b64encode(buffer).decode('utf-8')}"
        except Exception as e:
            print(f"Error al convertir la imagen a Base64: {str(e)}")
            return None

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            image_base64 = data.get("image_base64")

            if not image_base64 or not isinstance(image_base64, str):
                return Response(
                    {"status": "Error", "message": "Imagen base64 no válida o vacía"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if image_base64.startswith('data:image'):
                if ',' not in image_base64:
                    return Response(
                        {"status": "Error", "message": "Formato de imagen base64 inválido"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                image_base64 = image_base64.split(",")[1]

            try:
                image_data = base64.b64decode(image_base64)
            except Exception as e:
                return Response(
                    {"status": "Error", "message": f"Error al decodificar la imagen base64: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            np_array = np.frombuffer(image_data, np.uint8)
            try:
                img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            except cv2.error as e:
                return Response(
                    {"status": "Error", "message": f"Error de OpenCV: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            if img is None:
                return Response(
                    {"status": "Error", "message": "No se pudo procesar la imagen. Verifica el formato."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                decoded_objects = decode(img)
            except Exception as e:
                return Response(
                    {"status": "Error", "message": f"Error en la biblioteca pyzbar: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            if not decoded_objects:
                return Response(
                    {"status": "Error", "message": "No se detectó ningún código QR"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                qr_data = decoded_objects[0].data.decode('utf-8')
            except UnicodeDecodeError as e:
                return Response(
                    {"status": "Error", "message": f"Error al decodificar el contenido del QR: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Buscar si el QR ya está registrado
            qr_record, created = QRRecord.objects.get_or_create(qr_data=qr_data)

            if created or qr_record.estado == "salida":
                # Registrar entrada
                qr_record.estado = "entrada"
                qr_record.hora_entrada = now()
                qr_record.hora_salida = None
                qr_record.tiempo_dentro = None  # Reiniciar el tiempo
                qr_record.save()
                processed_base64 = self.convertir_imagen_a_base64(img)
                return Response(
                    {
                        "status": "Success",
                        "message": f"Entrada registrada para QR: {qr_data}",
                        "processed_image": processed_base64
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        "status": "Complete",
                        "message": "El QR ya fue procesado como entrada."
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {"status": "Error", "message": f"Ha ocurrido un error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class QRSalidaView(APIView):
    """
    Procesa la salida de un QR.
    """
    def convertir_imagen_a_base64(self, imagen_cv2):
        try:
            success, buffer = cv2.imencode('.png', imagen_cv2)
            if not success:
                raise ValueError("No se pudo codificar la imagen a formato PNG")
            return f"data:image/png;base64,{base64.b64encode(buffer).decode('utf-8')}"
        except Exception as e:
            print(f"Error al convertir la imagen a Base64: {str(e)}")
            return None

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            image_base64 = data.get("image_base64")

            if not image_base64 or not isinstance(image_base64, str):
                return Response({"status": "Error", "message": "Imagen base64 no válida o vacía"}, status=status.HTTP_400_BAD_REQUEST)

            if image_base64.startswith('data:image'):
                if ',' not in image_base64:
                    return Response({"status": "Error", "message": "Formato de imagen base64 inválido"}, status=status.HTTP_400_BAD_REQUEST)
                image_base64 = image_base64.split(",")[1]

            try:
                image_data = base64.b64decode(image_base64)
            except Exception as e:
                return Response({"status": "Error", "message": f"Error al decodificar la imagen base64: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            np_array = np.frombuffer(image_data, np.uint8)
            try:
                img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            except cv2.error as e:
                return Response({"status": "Error", "message": f"Error de OpenCV: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if img is None:
                return Response({"status": "Error", "message": "No se pudo procesar la imagen. Verifica el formato."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                decoded_objects = decode(img)
            except Exception as e:
                return Response({"status": "Error", "message": f"Error en la biblioteca pyzbar: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if not decoded_objects:
                return Response({"status": "Error", "message": "No se detectó ningún código QR"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                qr_data = decoded_objects[0].data.decode('utf-8')
            except UnicodeDecodeError as e:
                return Response({"status": "Error", "message": f"Error al decodificar el contenido del QR: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            qr_record = QRRecord.objects.filter(qr_data=qr_data).first()

            if qr_record is None:
                return Response({"status": "Error", "message": "El QR no está registrado para entrada o salida."}, status=status.HTTP_400_BAD_REQUEST)

            if qr_record.estado == "entrada" and not qr_record.hora_salida:
                qr_record.estado = "salida"
                qr_record.hora_salida = now()
                tiempo_transcurrido = qr_record.hora_salida - qr_record.hora_entrada

                total_seconds = int(tiempo_transcurrido.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                tiempo_legible = f"{hours}h {minutes}m {seconds}s"

                qr_record.tiempo_dentro = tiempo_transcurrido
                qr_record.tiempo_legible = tiempo_legible
                qr_record.save()

                processed_base64 = self.convertir_imagen_a_base64(img)
                return Response(
                    {
                        "status": "Success",
                        "message": f"Salida registrada para QR: {qr_data}",
                        "processed_image": processed_base64,
                        "tiempo_dentro": tiempo_legible
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"status": "Complete", "message": "El QR ya fue procesado como salida."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": "Error", "message": f"Ha ocurrido un error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QRCodeAPI(APIView):
    def post(self, request):
        serializer = QRCodeSerializer(data=request.data)
        if serializer.is_valid():
            nombres = serializer.validated_data["nombres"]
            apellidos = serializer.validated_data["apellidos"]
            documento = serializer.validated_data["documento"]

            # Crear el contenido del código QR
            data = f"{nombres} {apellidos},{documento}"

            # Generar el código QR
            try:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(data)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                # Agregar el prefijo data:image/png;base64,
                img_base64 = f"data:image/png;base64,{base64_image}"

                # Guardar en la base de datos
                qr_data = QRCodeData.objects.create(
                    nombres=nombres,
                    apellidos=apellidos,
                    documento=documento,
                    qr_code_base64=img_base64
                )
                qr_data.save()

                return Response({
                    "message": "QR generado y guardado correctamente",
                    "qr_code_base64": img_base64
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({
                    "error": "No se pudo generar el código QR",
                    "details": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def descargar_qr(request, filename):
    try:
        qr_data = QRCodeData.objects.get(documento=filename)
        img_base64 = qr_data.qr_code_base64
        
        # Eliminar el prefijo si existe
        if img_base64.startswith("data:image/png;base64,"):
            img_base64 = img_base64.split(",")[1]
        
        img_data = base64.b64decode(img_base64)
        response = HttpResponse(img_data, content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename={filename}.png'
        return response
    except QRCodeData.DoesNotExist:
        return HttpResponse("QR no encontrado", status=404)


# Generar código QR y devolver la representación base64
def generar_codigo_qr(data):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return {"success": True, "qr_code_base64": img_base64}
    except Exception as e:
        return {"success": False, "error": str(e)}
