import csv
import os
import random
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# Nombre del archivo CSV
file_name = "../data_bda/csv/sales_data.csv"

# Asegurar que el directorio existe
os.makedirs(os.path.dirname(file_name), exist_ok=True)

# Número de registros a generar
num_records = 1000

# Definimos las probabilidades de errores y valores nulos
null_probability = 0.05  # 5% de valores nulos
error_probability = 0.02  # 2% de errores de formato

# Función para introducir errores en Product ID
def generate_product_id():
    if random.random() < error_probability:
        return fake.word()  # Introducir un error (palabra en lugar de alfanumérico)
    return fake.bothify(text="??-#####")

# Función para generar valores con posibles nulos
def maybe_null(value):
    return "" if random.random() < null_probability else value

# Crear y escribir en el archivo CSV
with open(file_name, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Escribir encabezados
    writer.writerow(["Date", "Store ID", "Product ID", "Quantity Sold", "Revenue"])
    
    for _ in range(num_records):
        date = maybe_null(fake.date())
        store_id = maybe_null(str(random.randint(1, 100)))
        product_id = maybe_null(generate_product_id())
        quantity_sold = maybe_null(str(random.randint(1, 50)))
        revenue = maybe_null(str(round(random.uniform(5, 500), 2)))
        
        writer.writerow([date, store_id, product_id, quantity_sold, revenue])

print(f"Archivo '{file_name}' generado con {num_records} registros.")