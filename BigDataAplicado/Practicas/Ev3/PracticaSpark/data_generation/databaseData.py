import psycopg2
import random
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# Crear datos en PostgreSQL con errores y nulos

# Número de registros a generar
num_records = 1000

# Probabilidades de errores y valores nulos
null_probability = 0.05  # 5% de valores nulos
error_probability = 0.02  # 2% de errores de formato

# Función para generar valores con posibles nulos
def maybe_null(value):
    return None if random.random() < null_probability else value

# Función para introducir errores en store_name
def generate_store_name():
    if random.random() < error_probability:
        return str(random.randint(1000, 9999))  # Error: número en lugar de nombre
    return fake.company()

# Conectar a PostgreSQL y crear la tabla
try:
    conn = psycopg2.connect(
        host="localhost",
        database="retail_db",
        user="postgres",
        password="casa1234",
        port=5432
    )
    cur = conn.cursor()
    
    # Crear tabla si no existe
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Stores (
            store_id SERIAL PRIMARY KEY,
            store_name TEXT,
            location TEXT,
            demographics TEXT
        );
    """)
    
    # Insertar datos generados
    for _ in range(num_records):
        store_name = maybe_null(generate_store_name())
        location = maybe_null(fake.city())
        demographics = maybe_null(fake.sentence())
        
        cur.execute(
            "INSERT INTO Stores (store_name, location, demographics) VALUES (%s, %s, %s)",
            (store_name, location, demographics)
        )
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Se han insertado {num_records} registros en la tabla Stores.")
    
except Exception as e:
    print("Error al conectar a la base de datos:", e)