import { useState } from "react";
import {useNavigate} from "react-router-dom";
import axios from "axios";
import Footer from "../footer/Footer"; 
import "./StylesFormFace.css"; 

const RegistrarRostro = () => {
  const navigate = useNavigate();
  const [nombre, setNombre] = useState("");
  const [cedula, setCedula] = useState("");
  const [whatsapp, setWhatsapp] = useState("");
  const [imagen, setImagen] = useState(null);
  const [mensaje, setMensaje] = useState("");

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onloadend = () => {
      setImagen(reader.result); // Eliminar el prefijo de Base64
    };

    if (file) {
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMensaje("");

    if (!nombre || !cedula || !whatsapp || !imagen) {
      setMensaje("Por favor, complete todos los campos.");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/facial/registrarRostros/", {
        nombre,
        cedula,
        whatsapp,
        image_base64: imagen,
      });

      setMensaje(response.data.message);
    } catch (error) {
      if (error.response) {
        setMensaje(error.response.data.message || "Error al registrar el rostro.");
      } else {
        setMensaje("Error interno del servidor.");
      }
    }
  };

  return (
    <div className="container-s">
      <div className="header-container">
          <img 
          src="https://ww1.aulavirtualuniversitariadecolombia.co/pluginfile.php/1/theme_klassroom/logo/1732826367/thumbnail_logo-universidad_balnco40px.png"
          alt="logo"
          className="header-form-logo"
        />
        </div>

      <div className="form-card-s">
      <h2 className="title-s">Registrar Rostro</h2>
        <form onSubmit={handleSubmit} className="form-layout-s">
        <div className="input-section-s">
          <div className="input-group-s">
            <label htmlFor="nombre">Nombre:</label>
            <input
              type="text"
              id="nombre"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              required
            />
          </div>
          <div className="input-group-s">
            <label htmlFor="cedula">Cédula:</label>
            <input
              type="text"
              id="cedula"
              value={cedula}
              onChange={(e) => setCedula(e.target.value)}
              required
            />
             </div>
          <div className="input-group-s">
            <label htmlFor="whatsapp">Numero de telefono:</label>
            <input
              type="text"
              id="whatsapp"
              value={whatsapp}
              onChange={(e)=> setWhatsapp(e.target.value)}
              required
            />
          </div>
    
            </div>
            <div className="image-upload-s">
                <label htmlFor="imagen">Imagen de rostro:</label>
                <div className="upload-box-s" onClick={() => document.getElementById('imagen').click()}>
                <img src="/imgs/subir-imagen (1).png"  alt="Hoja" className="upload-icon" />
                  <p className="upload-text-s">Imagen de 2MB.</p>
                  <button className="upload-button-s">Subir</button>
                </div>
                <input
                  type="file"
                  id="imagen"
                  accept="image/*"
                  onChange={handleImageChange}
                  required
                  hidden
                />
              </div>

        </form>
        <div className="buttons-s">
          <button className="btn btn-b-s" onClick={() => navigate("/")}>Atrás</button>
          <button type="submit" className="btn btn-register-s">Registrar</button>
        </div>
        {mensaje && <p className="message">{mensaje}</p>}
      </div>
      <Footer />
    </div>
  );
};

export default RegistrarRostro;
