import csv
from faker import Faker
import random
import json

# Inicializar el generador Faker
fake = Faker()

# Nombre del archivo de salida
horarios = "./datos/horarios.csv"

# Abrir el archivo en modo escritura
with open(horarios, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Escribir los encabezados del CSV
    writer.writerow(['linea', 'hora_inicio', 'hora_fin'])
    i = 1
    # Generar y escribir 100 registros
    for _ in range(100):
        linea =  f'L{i}'
        hora_inicio = f'{random.randint(1, 24)}:{random.randint(1, 60)}'
        hora_fin = f'{random.randint(1, 24)}:{random.randint(1, 60)}'
        writer.writerow([linea, hora_inicio, hora_fin])
        i=i+1
print(f"Archivo CSV generado: {horarios}")


conductores = "./datos/conductores.txt"
vehiculo = ['Bus_','Tranvia_']


# Abrir el archivo en modo escritura
with open(conductores, mode='w') as file:
    # Generar y escribir 2000 registros
    i = 1
    for _ in range(2000):
        id_conductor = f'C{i}'
        nombre = fake.name()
        vehiculo = f'{fake.random_element(['Bus_','Tranvia_'])}{random.randint(1, 100)}' 
        linea =  f'L{random.randint(1, 100)}'
        file.write(f"{id_conductor},{nombre},{vehiculo},{linea}\n")
        i= i+1

print(f"Archivo TXT generado: {conductores}")


# Nombre del archivo de salida
tarifas = "./datos/tarifas.json"

# Lista para almacenar los registros
data = []

# Generar 100 registros
for _ in range(100):
    record = {
        "linea": f'L{random.randint(1, 100)}',
        "precio": fake.random_element([1.00,1.25,1.50,1.75,2.00]),
        "descuento": fake.random_element([0.10,0.20,0.30,0.40,0.50]),
    }
    data.append(record)

# Escribir los registros en formato JSON
with open(tarifas, mode='w') as file:
    json.dump(data, file, indent=4)

print(f"Archivo JSON generado: {tarifas}")


