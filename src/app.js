const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Rutas
const facialRecognitionRoutes = require("./routes/facialRecognitionRoutes");
app.use("/api/facial-recognition", facialRecognitionRoutes);

// Ruta de prueba
app.get("/", (req, res) => {
    res.send("¡Hola, mundo desde Express!");
});

// Iniciar el servidor
app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
