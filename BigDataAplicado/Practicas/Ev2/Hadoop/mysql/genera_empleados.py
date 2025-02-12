import mysql.connector
from faker import Faker
import random

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",       # Cambia esto si tu base de datos no está en localhost
    user="root",            # Cambia esto con tu usuario de MySQL
    password="root",        # Cambia esto con tu contraseña de MySQL
    database="hadoop"       # Base de datos donde quieres insertar los datos
)

cursor = db.cursor()
fake = Faker()

# Lista de departamentos predefinidos
departamentos = [
    "Ventas", "Contabilidad", "Marketing", "Recursos Humanos", 
    "IT", "Finanzas", "Logística", "Atención al Cliente", 
    "Producción", "Investigación y Desarrollo", "Legal", "Compras"
]

# Generar e insertar 2000 registros en la tabla empleados
for i in range(1, 2001):
    nombre = fake.name()
    #departamento = fake.job()[:50]  # Limita el tamaño a 50 caracteres
    departamento = random.choice(departamentos)  # Selecciona un departamento al azar de la lista
    salario = round(random.uniform(30000, 120000), 2)
    fecha_contratacion = fake.date_between(start_date="-10y", end_date="today")
    
    # Crear la consulta para insertar los datos
    query = """
    INSERT INTO empleados (id, nombre, departamento, salario, fecha_contratacion)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    # Los valores para la inserción
    values = (i, nombre, departamento, salario, fecha_contratacion)
    
    # Ejecutar la inserción
    cursor.execute(query, values)

# Confirmar las inserciones en la base de datos
db.commit()

# Cerrar la conexión
cursor.close()
db.close()

print("2000 registros insertados con éxito en la tabla 'empleados'.")
