from binascii import Error
import csv
import json
import mysql.connector
import requests
from faker import Faker
import random

def connect_to_mysql(host='localhost', user='root', password='root', database=None): # my-secret-pw
    """Conecta a MySQL y devuelve la conexión."""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306,
            auth_plugin='mysql_native_password'  # 🔹 Agregamos esta línea para evitar errores
        )
        if connection.is_connected():
            print("✅ Conexión exitosa a MySQL")
            return connection
    except Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        return None

def create_database(db_name):
    """Crea una base de datos si no existe."""
    connection = connect_to_mysql()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"📂 Base de datos '{db_name}' creada o ya existente.")
        except Error as e:
            print(f"❌ Error al crear la base de datos: {e}")
        finally:
            cursor.close()
            connection.close()

def create_table(db_name, table_name, schema):
    """Crea una tabla en la base de datos."""
    connection = connect_to_mysql(database=db_name)
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
            print(f"📋 Tabla '{table_name}' creada en '{db_name}'.")
        except Error as e:
            print(f"❌ Error al crear la tabla: {e}")
        finally:
            cursor.close()
            connection.close()

def insert_data(db_name, table_name, columns, values):
    """Inserta datos en una tabla."""
    connection = connect_to_mysql(database=db_name)
    if connection:
        try:
            cursor = connection.cursor()
            placeholders = ', '.join(['%s'] * len(values))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(query, values)
            connection.commit()
            print("✅ Datos insertados correctamente.")
        except Error as e:
            print(f"❌ Error al insertar datos: {e}")
        finally:
            cursor.close()
            connection.close()

def insert_data_from_csv(db_name, table_name, columns, csv_file):
    """Inserta datos en una tabla desde un archivo CSV."""
    connection = connect_to_mysql(database=db_name)
    if connection:
        try:
            cursor = connection.cursor()
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Saltar la cabecera si existe
                for row in reader:
                    placeholders = ', '.join(['%s'] * len(row))
                    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                    cursor.execute(query, row)
            connection.commit()
            print("✅ Datos insertados desde CSV correctamente.")
        except Error as e:
            print(f"❌ Error al insertar datos desde CSV: {e}")
        finally:
            cursor.close()
            connection.close()

def insert_data_from_json(db_name, table_name, columns, json_file):
    """Inserta datos en una tabla desde un archivo JSON."""
    connection = connect_to_mysql(database=db_name)
    if connection:
        try:
            cursor = connection.cursor()
            with open(json_file, encoding='utf-8') as file:
                data = json.load(file)
                for entry in data:
                    values = tuple(entry[col] for col in columns)
                    placeholders = ', '.join(['%s'] * len(values))
                    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                    cursor.execute(query, values)
            connection.commit()
            print("✅ Datos insertados desde JSON correctamente.")
        except Error as e:
            print(f"❌ Error al insertar datos desde JSON: {e}")
        finally:
            cursor.close()
            connection.close()

def insert_data_from_txt(db_name, table_name, columns, txt_file, delimiter='|'):
    """Inserta datos en una tabla desde un archivo TXT delimitado."""
    connection = connect_to_mysql(database=db_name)
    if connection:
        try:
            cursor = connection.cursor()
            with open(txt_file, encoding='utf-8') as file:
                for line in file:
                    values = tuple(line.strip().split(delimiter))
                    placeholders = ', '.join(['%s'] * len(values))
                    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                    cursor.execute(query, values)
            connection.commit()
            print("✅ Datos insertados desde TXT correctamente.")
        except Error as e:
            print(f"❌ Error al insertar datos desde TXT: {e}")
        finally:
            cursor.close()
            connection.close()

def generarDatos():
    fake = Faker()
    # Nombre del archivo de salida
    datos = "./archivos/mysqlGen.csv"
    
    # Abrir el archivo en modo escritura
    with open(datos, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Escribir los encabezados del CSV
        writer.writerow(['linea', 'hora_inicio', 'hora_fin'])
        i = 1
        # Generar y escribir 100 registros
        for _ in range(2000):
            id = i
            vehiculo = f'{fake.random_element(['Bus_','Tranvia_'])}{random.randint(1, 100)}'
            linea =  f'L{random.randint(1, 100)}'
            monto = fake.random_element([1.00,1.25,1.50,1.75,2.00])
            fecha = fake.date_time()
            writer.writerow([id, vehiculo, linea, monto, fecha])
            i=i+1

    print(f"Archivo CSV generado: {datos}")


# 🛠️ EJEMPLO DE USO
if __name__ == "__main__":
    create_database('transporte')
    create_table('transporte', 'tickets', 'id INT AUTO_INCREMENT PRIMARY KEY, vehiculo VARCHAR(255), linea VARCHAR(255), monto FLOAT, fecha DATETIME')
    generarDatos()
    insert_data_from_csv('transporte', 'tickets', ['id', 'vehiculo','linea','monto','fecha'], './archivos/mysqlGen.csv')
