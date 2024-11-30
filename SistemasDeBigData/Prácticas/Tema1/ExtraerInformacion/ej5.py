import cv2
import matplotlib.pyplot as plt

# 1. Detección y Localización de Objetos en las Imágenes (Ejemplo: Detección de Rostros)
def detectar_objetos(imagen_path):
    # Cargar el clasificador Haar Cascade pre-entrenado
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Leer la imagen
    imagen = cv2.imread(imagen_path)

    if imagen is None:
        print(f"Error: No se pudo cargar la imagen en la ruta {imagen_path}")
        return

    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en la imagen
    rostros = face_cascade.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5)

    # Dibujar un rectángulo alrededor de los rostros detectados
    for (x, y, w, h) in rostros:
        cv2.rectangle(imagen, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Mostrar la imagen con los rostros detectados
    plt.imshow(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title(f"Detección de Rostros - {imagen_path}")
    plt.show()

# 2. Reconocimiento de Patrones en las Imágenes (Ejemplo: Detección de Puntos Clave con ORB)
def reconocimiento_patrones(imagen_path):
    # Leer la imagen
    imagen = cv2.imread(imagen_path)

    if imagen is None:
        print(f"Error: No se pudo cargar la imagen en la ruta {imagen_path}")
        return

    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Crear el detector ORB
    orb = cv2.ORB_create()

    # Detectar los puntos clave y sus descriptores
    keypoints, descriptors = orb.detectAndCompute(gris, None)

    # Dibujar los puntos clave en la imagen
    imagen_con_puntos = cv2.drawKeypoints(imagen, keypoints, None, color=(0, 255, 0))

    # Mostrar la imagen con los puntos clave
    cv2.imshow(f'Imagen con puntos clave - {imagen_path}', imagen_con_puntos)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Función principal
def main():
    # Lista de imágenes a procesar
    imagen_paths = ["Imagenes/imagen1.png", "Imagenes/imagen2.png", "Imagenes/imagen3.png"]  # Cambia/Añade las rutas de tus imágenes

    for imagen_path in imagen_paths:
        print(f"Procesando {imagen_path}...")

        print("Iniciando detección de objetos en la imagen...")
        detectar_objetos(imagen_path)

        print("Iniciando reconocimiento de patrones en la imagen...")
        reconocimiento_patrones(imagen_path)

    input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
