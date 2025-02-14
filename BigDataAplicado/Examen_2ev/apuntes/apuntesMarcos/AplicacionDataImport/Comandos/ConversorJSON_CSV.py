import json
import csv
import tkinter as tk
from tkinter import filedialog
import os

class Conversor:
    
    def flatten_dict(self, d, parent_key='', sep='.'):
        """Aplana un diccionario anidado."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())  # Recursión para dict anidados
            else:
                items.append((new_key, v))
        return dict(items)

    def convertir_json_a_csv(self, json_file_path, csv_file_path):
        """Leer un archivo JSON y escribirlo como un archivo CSV."""
        rows = []
        
        # Intentar abrir y cargar el archivo JSON
        try:
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                datos_json = json.load(json_file)  # Leemos el archivo completo (no línea por línea)

            # Aplanar las claves del objeto JSON y agregarlo a la lista de filas
            for item in datos_json:
                fila = self.flatten_dict(item)  # Asegúrate de que flatten_dict está correctamente implementado
                rows.append(fila)

        except json.JSONDecodeError as e:
            print(f"Error al procesar el archivo JSON: {e}")
            return
        except FileNotFoundError:
            print(f"El archivo {json_file_path} no se encuentra.")
            return

        # Si no se encontraron filas, salir
        if not rows:
            print("No se encontraron datos válidos en el archivo JSON.")
            return

        # Escribir los datos a un archivo CSV
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print(f"Los datos se han guardado correctamente en {csv_file_path}.")


    def seleccionar_archivo_json(self):
        """Abrir una ventana de diálogo para seleccionar un archivo JSON."""
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter
        archivo_json = filedialog.askopenfilename(
            title="Selecciona un archivo JSON",
            filetypes=[("Archivos JSON", "*.json")]
        )
        return archivo_json

    def guardar_archivo_csv(self, ruta_json):
        """Generar la ruta para guardar el archivo CSV con el mismo nombre en la misma ubicación."""
        nombre_csv = os.path.splitext(os.path.basename(ruta_json))[0] + '.csv'
        ruta_csv = os.path.join(os.path.dirname(ruta_json), nombre_csv)
        return ruta_csv

    def csv_to_json(self, csv_file, json_file):
        """Convierte un archivo CSV a JSON."""
        try:
            # Leer el archivo CSV
            with open(csv_file, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                # Crear una lista de diccionarios a partir del CSV
                data = [row for row in csv_reader]

            # Escribir el JSON en un archivo
            with open(json_file, mode='w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            print(f"Conversión completada. JSON guardado en '{json_file}'")

        except FileNotFoundError:
            print(f"El archivo '{csv_file}' no se encontró. Por favor, verifica el nombre y la ubicación.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")
