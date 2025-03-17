import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom"; 
import axios from "axios";
import "./FaceComponentEnter.css";

const FaceRecognitionEnter = () => {
  const [message, setMessage] = useState(""); // Mensaje del backend
  const [isProcessing, setIsProcessing] = useState(false); // Evitar múltiples solicitudes
  const [isCameraActive, setIsCameraActive] = useState(true); // Controlar si la cámara está activa
  const videoRef = useRef(null); // Referencia al video
  const canvasRef = useRef(null); // Referencia al canvas
  const navigate = useNavigate(); // Hook para redirigir rutas

  useEffect(() => {
    if (!isCameraActive) return;

    let intervalId;

    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "user" },
        });
        videoRef.current.srcObject = stream;
        videoRef.current.play();
        const context = canvasRef.current.getContext("2d");

        intervalId = setInterval(() => {
          if (videoRef.current && canvasRef.current && !isProcessing) {
            context.drawImage(
              videoRef.current,
              0,
              0,
              canvasRef.current.width,
              canvasRef.current.height
            );
            const imageData = canvasRef.current.toDataURL("image/png");
            sendFrameToBackend(imageData);
          }
        }, 1000); // Captura un frame por segundo
      } catch (error) {
        console.error("Error al acceder a la cámara:", error);
        setMessage("No se pudo acceder a la cámara.");
      }
    };

    startCamera();

    return () => {
      if (intervalId) clearInterval(intervalId);
      if (videoRef.current && videoRef.current.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks();
        tracks.forEach((track) => track.stop());
      }
    };
  }, [isProcessing, isCameraActive]);

  const sendFrameToBackend = async (base64Image) => {
    if (!isCameraActive) return;
    try {
      setIsProcessing(true);

      // Enviar la imagen al backend
      const response = await axios.post(
        "http://127.0.0.1:8000/facial/entrada/",
        {
          rostro_base64: base64Image, // Imagen en Base64
        }
      );

      setMessage(response.data.message);

      // Redirige a la nueva ruta si el backend confirma el reconocimiento
      if (response.data.status === "Success") {
        stopCamera();
        navigate("/Intermedio");
      }
    } catch (error) {
      console.error("Error al enviar la imagen al backend:", error);
      setMessage("Error al procesar la imagen.");
    } finally {
      setIsProcessing(false);
    }
  };

  const stopCamera = () => {
    setIsCameraActive(false); // Detener la captura de frames
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();
      tracks.forEach((track) => track.stop()); // Detener las pistas del video
    }
  };

  return (
    <div className="container-face-c">
      {isCameraActive ? (
        <div className="container-video-face">
          <video
            ref={videoRef}
            width="320"
            height="240"
            className="video-face-c"
          />
          <canvas
            ref={canvasRef}
            width="320"
            height="240"
            className="canva-face-c"
          />
        </div>
      ) : (
        <p>Cámara detenida.</p>
      )}
      <p className="message-face-c">{message}</p> {}
    </div>
  );
};

export default FaceRecognitionEnter;
