const express = require("express");
const router = express.Router();
const facialRecognitionController = require("../controllers/facialRecognitionController");

// Ruta para ejecutar el reconocimiento facial
router.post("/recognize", facialRecognitionController.recognizeFace);

module.exports = router;
