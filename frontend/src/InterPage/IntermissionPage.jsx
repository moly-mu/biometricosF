import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Footer from "../components/footer/Footer";
import "../InterPage/InterStyles.css";

const Intermission = () => {
  const [selectedExit, setSelectedExit] = useState(null);
  const navigate = useNavigate();

  const handleSelection = (method) => {
    setSelectedExit(method);
  };

  useEffect(() => {
    if (selectedExit === "facial") {
      navigate("/salidaFace");
    }
  }, [selectedExit, navigate]);

  return (
    <div className="container-inter">
      <div className="header-container">
        <img 
          src="https://ww1.aulavirtualuniversitariadecolombia.co/pluginfile.php/1/theme_klassroom/logo/1732826367/thumbnail_logo-universidad_balnco40px.png" 
          alt="logo" 
          className="header-form-logo" 
        />
      </div>
      
      <div className="app-container-intermission">
        <h2 className="title-inter">Sistema de Control de Acceso</h2>
      </div>
      <div className="main-inter">
        <h2 className="subtitle-inter">¿Estás seguro que quieres salir?</h2>

        <div className="button-container-inter">
          <button className="learn-more" onClick={() => handleSelection("facial")}>
          <span className="circle" aria-hidden="true">
              <span className="icon arrow"></span>
          </span>
          <span className="button-text">Salir</span>
          </button>
        </div>
      </div>
      <Footer />
      </div>
  );
};

export default Intermission;