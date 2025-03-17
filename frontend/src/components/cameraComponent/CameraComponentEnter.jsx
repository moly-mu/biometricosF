import { useState, useEffect, useRef } from "react";
import axios from "axios";
import jsQR from "jsqr";
import './CameraComponent.css'; 

const QRScanner = ({ onQRCodeDetected }) => {
  const [message, setMessage] = useState(""); // Mensaje del backend
  const [isProcessing, setIsProcessing] = useState(false); // Evitar múltiples solicitudes
  const [isScannerActive, setIsScannerActive] = useState(true); // Control del escáner
  const videoRef = useRef(null); // Referencia al video
  const canvasRef = useRef(null); // Referencia al canvas

  useEffect(() => {
    if (!isScannerActive) return;

    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "environment" },
        });
        videoRef.current.srcObject = stream;
        videoRef.current.play();

        const context = canvasRef.current.getContext("2d");

        const intervalId = setInterval(() => {
          if (videoRef.current && canvasRef.current && !isProcessing) {
            context.drawImage(
              videoRef.current,
              0,
              0,
              canvasRef.current.width,
              canvasRef.current.height
            );

            const imageData = context.getImageData(
              0,
              0,
              canvasRef.current.width,
              canvasRef.current.height
            );
            const code = jsQR(imageData.data, canvasRef.current.width, canvasRef.current.height);

            if (code) {
              setIsProcessing(true);
              sendQRCodeToBackend(); // Enviar solo el dato del QR al backend
              onQRCodeDetected(code.data); // Notificar al componente padre
            }
          }
        }, 500); // Procesar frames cada 500ms

        // Guardar referencia al intervalo para limpieza
        return () => clearInterval(intervalId);
      } catch (error) {
        console.error("Error al acceder a la cámara:", error);
        setMessage("No se pudo acceder a la cámara.");
      }
    };

    startCamera();

    // Limpiar al desmontar
    return () => stopScanner();
  }, [isScannerActive, isProcessing]);

  const sendQRCodeToBackend = async () => {
    if (!isScannerActive) return; // Verificar si el escáner sigue activo

    try {
      const canvas = canvasRef.current;
      const base64Image = canvas.toDataURL("image/png");

      const response = await axios.post("http://127.0.0.1:8000/qr_scanner_entrada/", {
        image_base64: base64Image,
      });

      setMessage(response.data.message);

      // Detener el escáner si el backend confirma el proceso
      if (response.data.status === "Success") {
        stopScanner();
      }
    } catch (error) {
      console.error("Error al enviar el QR al backend:", error);
      setMessage("Error al procesar el QR.");
    } finally {
      setIsProcessing(false);
    }
  };

  const stopScanner = () => {
    setIsScannerActive(false); // Desactivar escáner
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach((track) => track.stop());
    }
  };

  return (
    <div className="qr-container">
      <h1 className="qr-title">Escáner de Código QR</h1>
      {isScannerActive ? (
        <div className="qr-video-container">
          <video
            ref={videoRef}
            width="320"
            height="240"
            className="qr-video"
          />
          <canvas
            ref={canvasRef}
            width="320"
            height="240"
            className="qr-canvas"
          />
        </div>
      ) : (
        <p>No se detectó ningún QR.</p>
      )}
      <p className="qr-message">{message}</p>
    </div>
  );
};

export default QRScanner;
