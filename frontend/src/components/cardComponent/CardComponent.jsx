import { useState } from "react";
import { Link } from "react-router-dom";
import FormComponent from '../formComponent/FormComponent';
import Header from "../header/Header";
import Footer from "../footer/Footer";
import "./CardComponent.css";

const CardComponent = () => {
  const [mode, setMode] = useState(null); // Estado manejado internamente

  return (
    <div className="app-container-card">
      {/* Header */}
      <Header title="Sistema de Control de Acceso" />

      {/* Contenido principal */}
      <div className="content-container">
        {!mode ? (
          <div className="card">
            <h1 className="card-title">Estudiante</h1>
            <p className="card-subtitle">Registro de alumnos</p>
            <div className="card-actions">
              {/* Botón para registrar QR */}
              <Link to="/registrar">
                <button
                  className="register-button"
                  onClick={() => setMode("registrar")}
                >
                  Registrar QR
                </button>
              </Link>

              {/* Botón para registrar rostro */}
              <Link to="/registrarRostro">
                <button className="face-register-button">
                  Registrar Rostro
                </button>
              </Link>

              {/* Botón para registrar huella dactilar */}
              <button
                className="fingerprint-button"
                onClick={() => alert("Registro de huella dactilar en desarrollo")}
              >
                Registrar Huella
              </button>
            </div>
          </div>
        ) : (
          <FormComponent onBack={() => setMode(null)} />
        )}
      </div>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default CardComponent;
