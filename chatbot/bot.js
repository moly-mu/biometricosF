const express = require('express');
const { Client } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const app = express();
app.use(express.json());

const client = new Client();

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true }); // Muestra el código QR en la terminal
});

client.on('ready', () => {
    console.log('Cliente de WhatsApp listo!');
});

app.post('/enviar-mensaje', async (req, res) => {
    const { numero, mensaje } = req.body; // Extrae las variables del cuerpo de la solicitud

    if (!numero || !mensaje) {
        return res.status(400).json({ error: 'Faltan el número o el mensaje' });
    }

    try {
        // Envía el mensaje de WhatsApp
        const chatId = `${numero}@c.us`; 
        await client.sendMessage(chatId, mensaje);
        res.status(200).json({ success: true, message: 'Mensaje enviado correctamente' });
    } catch (error) {
        console.error('Error al enviar el mensaje:', error);
        res.status(500).json({ error: 'Error al enviar el mensaje' });
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Servidor del chatbot escuchando en http://localhost:${PORT}`);
});

client.initialize();