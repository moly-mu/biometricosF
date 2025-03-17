import { useState } from "react";
import axios from "axios";
import Header from "../header/Header";
import Footer from "../footer/Footer";

export default function RegistrarAsistencia() {
  const [usuarioId, setUsuarioId] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMensaje("");

    try {
      const response = await axios.post("/api/registrar_asistencia/", {
        usuario_id: usuarioId,
      });
      setMensaje(response.data.mensaje);
    } catch (error) {
      setMensaje(error.response?.data?.error || "Error al registrar asistencia");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center bg-gray-100 text-gray-800">
      <Header />
      <div className="flex-grow flex items-center justify-center w-full">
        <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
          <h2 className="text-xl font-bold text-center mb-4">Registrar Asistencia</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              value={usuarioId}
              onChange={(e) => setUsuarioId(e.target.value)}
              placeholder="ID del usuario"
              className="w-full p-2 border rounded-lg focus:ring focus:ring-blue-300"
              required
            />
            <button
              type="submit"
              className="w-full bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 transition"
              disabled={loading}
            >
              {loading ? "Registrando..." : "Registrar"}
            </button>
          </form>
          {mensaje && (
            <p className="mt-4 text-center text-sm font-medium text-gray-700">{mensaje}</p>
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
}
