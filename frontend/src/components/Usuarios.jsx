// Usuarios.js
import React, { useState } from 'react';
import axios from 'axios';
import FormComponent from './FormComponent'; // Importamos el formulario

const Usuarios = () => {
  const [usuarios, setUsuarios] = useState([]); // Estado para la lista de usuarios

  const baseUrl = "http://localhost:8000/api"; // URL base de tu API

  // Función para manejar el envío de datos
  const handleSubmit = async (formData) => {
    try {
      // Crear objeto FormData para enviar datos y archivos
      const data = new FormData();
      data.append("nombres", formData.nombres);
      data.append("apellidos", formData.apellidos);
      data.append("documento", formData.documento);

      if (formData.huella) data.append("huella", formData.huella);
      if (formData.codigoqr) data.append("codigoqr", formData.codigoqr);
      if (formData.rf) data.append("rf", formData.rf);

      // Enviar datos al backend
      const response = await axios.post(`${baseUrl}/usuarios/`, data, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      // Actualizar lista de usuarios si la respuesta es exitosa
      setUsuarios([...usuarios, response.data]);
      alert("Usuario registrado con éxito");
    } catch (error) {
      console.error("Error al registrar el usuario:", error);
      alert("Hubo un error al registrar el usuario");
    }
  };

  // Obtener usuarios existentes
  const fetchUsuarios = async () => {
    try {
      const response = await axios.get(`${baseUrl}/usuarios/`);
      setUsuarios(response.data);
    } catch (error) {
      console.error("Error al obtener usuarios:", error);
    }
  };

  // useEffect para cargar los usuarios al iniciar el componente (si es necesario)
  React.useEffect(() => {
    fetchUsuarios();
  }, []);

  return (
    <div>
      <h1>Gestión de Usuarios</h1>

      {/* Formulario para registrar nuevos usuarios */}
      <FormComponent
        onSubmit={handleSubmit} // Pasamos la función handleSubmit
      />

      {/* Mostrar lista de usuarios registrados */}
      <div>
        <h2>Usuarios Registrados</h2>
        <ul>
          {usuarios.map((usuario) => (
            <li key={usuario.documento}>
              {usuario.nombres} {usuario.apellidos} - {usuario.documento}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Usuarios;
