import cv2
import face_recognition
import pickle
import os
import sys
import json

# Archivo para almacenar codificaciones de rostros conocidos
KNOWN_FACES_FILE = "rostros_conocidos.pkl"

# Función para cargar los rostros conocidos desde el archivo
def cargar_rostros_conocidos():
    if os.path.exists(KNOWN_FACES_FILE) and os.path.getsize(KNOWN_FACES_FILE) > 0:
        with open(KNOWN_FACES_FILE, "rb") as f:
            return pickle.load(f)
    return [], []

# Función para guardar los rostros conocidos en el archivo
def guardar_rostros_conocidos(encodings, names):
    with open(KNOWN_FACES_FILE, "wb") as f:
        pickle.dump((encodings, names), f)

# Cargar codificaciones y nombres conocidos
known_face_encodings, known_face_names = cargar_rostros_conocidos()

# Inicializar la cámara (prueba con diferentes índices: 0, 1, 2)
video_capture = cv2.VideoCapture(2)  # Cambia el índice si no funciona
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Ajusta la resolución
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Captura un solo frame de video
ret, frame = video_capture.read()

# Verificar si la cámara está accesible
if not ret:
    print(json.dumps({"error": "No se pudo acceder a la cámara."}))
    sys.exit(1)

# Descomenta esta sección si necesitas verificar la imagen de la cámara manualmente
# Muestra temporalmente el cuadro para verificar el acceso y la iluminación
# cv2.imshow("Prueba de Cámara", frame)
# cv2.waitKey(1000)  # Muestra la imagen por 1 segundo
# cv2.destroyAllWindows()

# Convertir el frame de BGR a RGB (formato requerido por face_recognition)
rgb_frame = frame[:, :, ::1]

# Detectar ubicaciones de rostros en el frame
face_locations = face_recognition.face_locations(rgb_frame)
face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

# Verificar si se detectaron rostros
if not face_locations:
    print(json.dumps({"message": "No se detectaron rostros"}))
    sys.exit(0)

# Resultado para enviar a Express
result = []

# Procesar cada rostro detectado
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Desconocido"
    
    # Si hay coincidencias, asigna el nombre correspondiente
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]
    else:
        # Si no hay coincidencias y se pasa un nombre como argumento, se guarda el nuevo rostro
        if len(sys.argv) > 1:
            name = sys.argv[1]
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)
            guardar_rostros_conocidos(known_face_encodings, known_face_names)
    
    # Agregar el resultado de cada rostro detectado
    result.append({
        "name": name,
        "location": {"top": top, "right": right, "bottom": bottom, "left": left}
    })

# Liberar la cámara y cerrar ventanas
video_capture.release()
cv2.destroyAllWindows()

# Imprimir el resultado en formato JSON para que Express pueda leerlo
print(json.dumps(result))
