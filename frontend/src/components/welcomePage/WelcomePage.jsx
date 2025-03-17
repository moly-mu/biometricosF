import { useState, useEffect } from 'react';
import FaceRecognitionEnter from '../faceComponent/FaceComponentEnter';
import Footer from '../footer/Footer';  
import './WelcomePage.css';

const WelcomePage = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [isVisible, setIsVisible] = useState(false);  // Estado para la animación

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.body.classList.toggle('dark-mode');
  };

  // Activar la animación cuando el componente se monte
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(true);  // Después de un pequeño retraso, activamos la animación
    }, 200);  // Ajusta este tiempo según prefieras

    return () => clearTimeout(timer);  // Limpiar el temporizador si se desmonta el componente
  }, []);

  return (
    <div className={`app-container-welcome ${darkMode ? 'dark-mode' : ''}`}>

      {/* Contenedor de imagen y botón como "navbar" */}
      <div className="header-container">
        <img 
          src="https://ww1.aulavirtualuniversitariadecolombia.co/pluginfile.php/1/theme_klassroom/logo/1732826367/thumbnail_logo-universidad_balnco40px.png"
          alt="logo"
          className="header-form-logo"
        />
        <button className="dark-mode-toggle" onClick={toggleDarkMode}>
          {darkMode ? '☀️' : '🌙'}
        </button>
      </div>
      <h1 className={`text-animation ${isVisible ? 'visible' : ''}`}>IUDC Sistema de Control <br></br>de Acceso Entrada</h1>
      <main className="main-content">
        {/* Aplicamos la clase de animación a los textos */}
        

        {/* Contenedor centrado para FaceRecognitionEnter */}
        <div className="face-recognition-container">
          <FaceRecognitionEnter mode="Entrada" />
        </div>
        <h2 className={`title text-animation ${isVisible ? 'visible' : ''}`}>Reconocimiento <br></br>Facial</h2>
      </main>

      <Footer />
    </div>
  );
};

export default WelcomePage;




     