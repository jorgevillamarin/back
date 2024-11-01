const { spawn } = require('child_process');

exports.recognizeFace = (req, res) => {
    const newName = req.body.name || "Desconocido";

    // Ejecuta el script de Python y pasa el nombre como argumento
    const pythonProcess = spawn('python3', ['src/script/reconocimiento_facial.py', newName]);

    let dataToSend = '';

    // Captura la salida del script de Python
    pythonProcess.stdout.on('data', (data) => {
        dataToSend += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Error en el script de Python: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            return res.status(500).send('Error al ejecutar el script de Python');
        }
        // Enviar la salida del script de Python (JSON) al cliente
        res.send(JSON.parse(dataToSend));
    });
};
