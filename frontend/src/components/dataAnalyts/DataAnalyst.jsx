import { useState, useEffect } from "react";
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import Footer from "../footer/Footer";
import './DataAnalyst.css'

const AsistenciaDashboard = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/data/reporte_general_uno/")
      .then(response => {
        console.log("📊 Datos recibidos (CSV):", response.data);

        // Convertir CSV en array de objetos
        const lines = response.data.split("\n").filter(line => line.trim() !== "");
        const headers = lines[0].split(",");

        // Verificar estructura del CSV
        if (headers.length < 4) {
          console.error("⚠️ Estructura CSV inesperada:", headers);
          return;
        }

        const formattedData = lines.slice(1).map(line => {
          const values = line.split(",");
          return {
            Bloque: values[0].trim(), // Nombre del bloque (Ej: "Bloque Uno")
            A_Tiempo: Number(values[1].trim()) || 0,
            Tarde: Number(values[2].trim()) || 0,
            Fuera_De_Horario: Number(values[3].trim()) || 0,
          };
        });

        console.log("✅ Datos procesados:", formattedData);
        setData(formattedData);
      })
      .catch(error => {
        console.error("❌ Error al cargar datos", error);
        setData([]);
      });
  }, []);

  // Función para descargar el reporte general en CSV
  const descargarCSV = async () => {
    const fechaInicio = "2024-02-01";
    const fechaFin = "2024-02-10";

    try {
      const response = await axios.get(`http://127.0.0.1:8000/data/reporte_general_uno/?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `reporte_asistencia_${fechaInicio}_${fechaFin}.csv`);
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error("Error al descargar el reporte:", error);
    }
  };
  //Descargar tabla docentes

  const descargarprofesCSV = async () => {
    const fechaInicio = "2024-02-01"; 
    const fechaFin = "2024-02-10";

    try {
      const response = await axios.get(`http://127.0.0.1:8000/data/reporte_asistencia/?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`, {
        responseType: "blob",
      });
    
      // Crear y descargar el archivo CSV
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `reporte_asistencia_${fechaInicio}_${fechaFin}.csv`);
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error("Error al descargar el reporte:", error);
    }
  };    
  
  return (
      <div className="container-dt">
        <div className="main-content">
        <div className="im-container">
        <img 
          src="https://ww1.aulavirtualuniversitariadecolombia.co/pluginfile.php/1/theme_klassroom/logo/1732826367/thumbnail_logo-universidad_balnco40px.png" 
          alt="logo" 
          className="im-logo" 
        />
      </div>
          <h2 className="title-dt">Estado de Asistencia por Bloques</h2>
          <div style={{ width: "100%", textAlign: "center", color: "black" }}>
            {data.length > 0 ? (
              <ResponsiveContainer width="100%" height={350}>
                <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="Bloque" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="A_Tiempo" fill="#6a5acd" name="A Tiempo" />
                  <Bar dataKey="Tarde" fill="#ff6347" name="Tarde" />
                  <Bar dataKey="Fuera_De_Horario" fill="#ffcc00" name="Fuera de Horario" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p>Cargando datos o sin información disponible...</p>
            )}
          </div>
    
          <div className="button-des">
            <button className="button-dcvs" onClick={descargarCSV}>
              Descargar Reporte CSV
            </button>
            <button className="button-prcvs" onClick={descargarprofesCSV}>
              Descargar asistencia CSV
            </button>
          </div>
        </div>
    
        <Footer/>
      </div>
  );
};

export default AsistenciaDashboard;
