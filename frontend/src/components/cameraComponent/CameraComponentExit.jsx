import { useState, useEffect, useRef } from "react";
import axios from "axios";
import jsQR from "jsqr"; // Librería para decodificar QR
import './CameraComponent.css'; 

const QRScanner = () => {
  const [message, setMessage] = useState(""); // Mensaje del backend
  const [qrData, setQrData] = useState(null); // Datos del QR detectado
  const [isProcessing, setIsProcessing] = useState(false); // Evitar múltiples solicitudes
  const [isScannerActive, setIsScannerActive] = useState(true); // Control del escáner
  const videoRef = useRef(null); // Referencia al video
  const canvasRef = useRef(null); // Referencia al canvas

  useEffect(() => {
    if (!isScannerActive) return; // Detener el escáner si no está activo

    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "environment" },
        });
        videoRef.current.srcObject = stream;
        videoRef.current.play();

        const context = canvasRef.current.getContext("2d");

        const detectQRCode = () => {
          if (!isScannerActive || isProcessing) return; // No continuar si el escáner está detenido o procesando

          if (videoRef.current && canvasRef.current) {
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
              setQrData(code.data); // Guardar los datos del QR detectado
              sendQRCodeToBackend(imageData); // Enviar la imagen del canvas
            }
          }
          if (isScannerActive) {
            requestAnimationFrame(detectQRCode); // Continuar escaneando si el escáner sigue activo
          }
        };

        detectQRCode();
      } catch (error) {
        console.error("Error al acceder a la cámara:", error);
        setMessage("No se pudo acceder a la cámara.");
      }
    };

    startCamera();

    // Detener la cámara al desmontar
    return () => stopScanner();
  }, [isScannerActive, isProcessing]);

  const sendQRCodeToBackend = async (imageData) => {
    try {
      setIsProcessing(true);

      // Convertir el canvas a Base64
      const canvas = canvasRef.current;
      const base64Image = canvas.toDataURL("image/png");

      // Enviar la imagen al backend
      const response = await axios.post("http://127.0.0.1:8000/qr_scanner_salida/", {
        image_base64: base64Image,
      });

      setMessage(response.data.message);

      // Detener el escáner si el backend confirma el proceso
      if (response.data.status === "Success") {
        stopScanner();
      }
    } catch (error) {
      console.error("Error al enviar la imagen al backend:", error.response?.data || error.message);
      if (error.response) {
        console.log("Detalles del error:", error.response.status, error.response.data);
      }
      setMessage("Error al procesar la imagen.");
    } finally {
      setIsProcessing(false);
    }
  };

  const stopScanner = () => {
    setIsScannerActive(false); // Detener la detección
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach((track) => track.stop()); // Detener las pistas del video
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
      ) : qrData ? (
        <div className="qr-result-container">
          <h2>QR Detectado:</h2>
          <p>{qrData}</p>
        </div>
      ) : (
        <p>No se detectó ningún QR.</p>
      )}
      {isProcessing && <p className="qr-processing">Procesando código QR...</p>}
      <p className="qr-message">{message}</p> {/* Mensaje con estilo en línea */}
    </div>
  );
};

export default QRScanner;
