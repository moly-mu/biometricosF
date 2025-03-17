import { useState } from "react";
import Header from "../components/header/Header";
import Footer from "../components/footer/Footer";
import FaceRecognition from "../components/faceComponent/FaceComponentExit";

const SegundoFactor = () => {
  const [selectedMethod, setSelectedMethod] = useState(null);

  const handleSelection = (method) => {
    setSelectedMethod(method);
  };

  const renderContent = () => {
    if (selectedMethod === "facial") {
      return <FaceRecognition />;
    } else if (selectedMethod === "huella") {
      return (
        <p>
          Funcionalidad de huella dactilar en desarrollo. Esta opción estará
          disponible en futuras versiones.
        </p>
      );
    } else {
      return <p>Seleccione un método para continuar.</p>;
    }
  };

  return (
    <div style={styles.container}>
      <Header />
      <div style={styles.titleContainer}>
        <h1 style={styles.title}>IUDC Control de Acceso Salida</h1>
      </div>
      <div style={styles.main}>
        <h2>Seleccione un método de autenticación</h2>
        <div style={styles.buttonContainer}>
          <button style={styles.button} onClick={() => handleSelection("facial")}>
            Reconocimiento Facial
          </button>
          <button style={styles.button} onClick={() => handleSelection("huella")}>
            Huella Dactilar
          </button>
        </div>
        <div style={styles.content}>{renderContent()}</div>
      </div>
      <Footer />
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    minHeight: "100vh",
    backgroundColor: "#002B5B",
    color: "white",
  },
  titleContainer: {
    backgroundColor: "#004B87",
    textAlign: "center",
    padding: "10px 0",
  },
  title: {
    margin: 0,
    color: "white",
    fontSize: "24px",
    fontWeight: "bold",
  },
  main: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: "20px",
    backgroundColor: "#1A1A1A",
  },
  buttonContainer: {
    display: "flex",
    gap: "10px",
    marginBottom: "20px",
  },
  button: {
    padding: "10px 20px",
    fontSize: "16px",
    color: "#FFF",
    backgroundColor: "#004B87",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
  content: {
    marginTop: "20px",
    textAlign: "center",
  },
};

export default SegundoFactor;
