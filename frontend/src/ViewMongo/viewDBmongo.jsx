import { useState } from "react";
import axios from "axios";
import Header from "../components/header/Header"; 
import Footer from "../components/footer/Footer";
import './viewDBmongo.css'

const ReporteAsistencia = () => {
    const [registros, setRegistros] = useState([]);
    const [cargando, setCargando] = useState([true]);
    const [error, setError] = useState(null);

    const obtenerRegistros = async () =>{
        setCargando(true);
        setError(null);

        try {
            const response = await axios.get("http://127.0.0.1:8000/data/basedatosvisual");
            setRegistros(response.data);
        } catch (err) {
            console.error("Error al obtener los datos:", err);
            setError("No se pudieron obtener los datos.");
        } finally {
            setCargando(false);
        }

    };

    // Función para regenerar el reporte y actualizar la tabla
    const regenerarReporte = async () => {
        setCargando(true);
        setError(null);

        try {
            await axios.get("http://127.0.0.1:8000/data/reporte_asistencia/");
            obtenerRegistros(); // Vuelve a cargar los datos actualizados
        } catch (err) {
            console.error("Error al regenerar el reporte:", err);
            setError("Error al regenerar el reporte.");
        } finally {
            setCargando(false);
        }
    };

    return (
        <div className="conteiner-repA">
        <Header />
        <main className="reporteA">
            <h2 className="titu-rep">Reporte de Asistencia</h2>

            <button
                onClick={regenerarReporte}
                className="button">
                Generar Reporte
            </button>

            {cargando ? (
                <p className="carga-datos">Cargando datos...</p>
            ) : error ? (
                <p className="error">{error}</p>
            ) : (
                <div className="datos">
                    <table className="tabla-datos">
                        <thead className="thr">
                            <tr>
                                <th className="tab-nombre">Nombre</th>
                                <th className="tab-horEntrada">Hora Entrada</th>
                                <th className="tab-horaSalida">Hora Salida</th>
                                <th className="tab-estado">Estado</th>
                            </tr>
                        </thead>
                        <tbody>
                            {registros.length > 0 ? (
                                registros.map((registro, index) => (
                                    <tr key={index} className="key">
                                        <td className="td-registroN">{registro.nombre}</td>
                                        <td className="td-horaE">{registro.hora_entrada || "N/A"}</td>
                                        <td className="td-horaS">{registro.hora_salida || "N/A"}</td>
                                        <td className={`border border-gray-300 px-4 py-2 font-semibold ${
                                            registro.estado === "A tiempo" ? "text-green-600" : "text-red-600"
                                        }`}>
                                            {registro.estado}
                                        </td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan="4" className="td-nhdd">
                                        No hay datos disponibles
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            )}
        </main>
        <Footer />
    </div>
);
};

export default ReporteAsistencia;

