
import random
from faker import Faker
from pymongo import MongoClient
import json
import csv
from pymongo.errors import ServerSelectionTimeoutError


def connect_to_mongo(host='localhost', port=27017, user='mongoadmin', password='secret', database=None):
    """Conecta a MongoDB y devuelve el cliente."""
    try:
        uri = f"mongodb://{user}:{password}@{host}:{port}/"
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)  # Añadimos un timeout para la selección de servidor
        client.server_info()  # Esto verifica la conexión al servidor MongoDB
        print("✅ Conexión exitosa a MongoDB")
        return client[database] if database else client
    except ServerSelectionTimeoutError as e:
        print(f"❌ Error al conectar a MongoDB: {e}")
        return None

def create_database(db_name):
    """Crea una base de datos en MongoDB (en realidad se crea cuando se insertan datos)."""
    client = connect_to_mongo()
    if client:
            db = client[db_name]
            print(f"📂 Base de datos '{db_name}' creada o ya existente.")
            return db

def create_collection(db_name, collection_name):
    """Crea una colección en la base de datos."""
    db = connect_to_mongo(database=db_name)
    if db is not None:
            collection = db[collection_name]
            print(f"📋 Colección '{collection_name}' creada en '{db_name}'.")
            return collection

def insert_data(db_name, collection_name, data):
    """Inserta datos en una colección."""
    db = connect_to_mongo(database=db_name)
    if db is not None:  # Cambiado aquí para evitar el error
            collection = db[collection_name]
            result = collection.insert_one(data)
            print(f"✅ Documento insertado con el ID: {result.inserted_id}")


def insert_data_from_json(db_name, collection_name, json_file):
    """Inserta datos en una colección desde un archivo JSON."""
    db = connect_to_mongo(database=db_name)
    if db is not None:
            collection = db[collection_name]
            with open(json_file, encoding='utf-8') as file:
                data = json.load(file)
                collection.insert_many(data)
            print("✅ Datos insertados desde JSON correctamente.")

def generarDatos():
     # Nombre del archivo de salida
    datos = "./archivos/mongoGen.json"
    # Inicializar el generador Faker
    fake = Faker()
    # Lista para almacenar los registros
    data = []

    # Generar 2000 registros
    for _ in range(2000):
        record = {
            "vehiculo": f'{fake.random_element(['Bus_','Tranvia_'])}{random.randint(1, 100)}',
            "latitud": str(fake.latitude()),
            "longitud": str(fake.longitude()),
            "timestamp": str(fake.date_time())
        }
        data.append(record)

    # Escribir los registros en formato JSON
    with open(datos, mode='w') as file:
        json.dump(data, file, indent=4)

    print(f"Archivo JSON generado: {datos}")

# 🛠️ EJEMPLO DE USO
if __name__ == "__main__":
    create_database('transporte')
    create_collection('transporte', 'posiciones')
    generarDatos()
    insert_data_from_json('transporte', 'posiciones','./archivos/mongoGen.json')

