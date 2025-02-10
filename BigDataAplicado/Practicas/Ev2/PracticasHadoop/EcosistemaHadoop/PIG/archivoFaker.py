from faker import Faker
import random
import csv

fake = Faker()

# Nombres de columnas
columns = ["Nombre", "Profesión", "Estado", "Valor"]

# Número de filas a generar
num_rows = 100

# Generar datos
data = []
for _ in range(num_rows):
    row = [
        fake.first_name(),
        random.choice(["Profesor", "Ingeniero", "Médico", "Abogado"]),
        random.choice(["Activo", "Inactivo"]),
        random.choice(["1", "0"])
    ]
    
    # Hacer aleatoriamente que una celda quede vacía
    null_index = random.randint(0, len(row) - 1)
    row[null_index] = ""
    
    data.append(row)

# Guardar en un archivo CSV
with open("datos.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(columns)  # Escribir encabezado
    writer.writerows(data)

print("Archivo datos.csv generado correctamente.")
