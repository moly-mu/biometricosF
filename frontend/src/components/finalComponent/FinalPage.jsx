import React from "react";
import FaceRecognitionExit from "../faceComponent/FaceComponentExit";
import Footer from '../footer/Footer';
import Header from '../header/Header';
import { motion } from "framer-motion";
import './FinalStyles.css';

const FinalPage = () => {

  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }} // Empieza fuera de la pantalla a la derecha
      animate={{ opacity: 1, x: 0 }}    // Aparece en el centro
      exit={{ opacity: 0, x: -100 }}    // Sale hacia la izquierda
      transition={{ duration: 0.5 }}    // Duración de la animación
    >

    <div className='app-container-final'>

      {/* Header */}
      <div>
        <Header title="Sistema de control de acceso Salida" />
      </div>

      {/*Camara */}
      <div className="camera-container">
        <FaceRecognitionExit mode="salida"/>
      </div>
      
      {/*Pie de pagina*/}
      <div>
        <Footer/>
      </div>
    </div>
    </motion.div>
  );
};

export default FinalPage;
