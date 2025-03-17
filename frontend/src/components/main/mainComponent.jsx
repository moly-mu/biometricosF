import { useState } from "react";
import QRScanner from "../faceComponent/FaceComponentEnter";
import FaceRecognition from "../cameraComponent/CameraComponentEnter";

const MainComponent = () => {
  const [qrData, setQrData] = useState(null); // Estado para almacenar el QR

  return (
    <div>
      <QRScanner setQrData={setQrData} />
      <FaceRecognition qrData={qrData} />
    </div>
  );
};

export default MainComponent;
