from pymongo import MongoClient
import json
from pywebhdfs.webhdfs import PyWebHdfsClient

# ---------- MONGO ----------

# Conexión a MongoDB
client = MongoClient("mongodb://mongoadmin:secret@localhost:27017/")
db = client['transporte']  # Cambia por tu base de datos
collection = db['posiciones']  # Cambia por tu colección

# Consulta MongoDB usando lookup (simulación de JOIN)
pipeline = [
    {
        "$lookup": {
            "from": "orders",  # Nombre de la colección a unir
            "localField": "user_id",  # Campo en la colección "users"
            "foreignField": "user_id",  # Campo correspondiente en "orders"
            "as": "user_orders"  # Nombre del nuevo campo que contendrá la lista de órdenes
        }
    },
    {
        "$match": {  # Filtro adicional, por ejemplo, para usuarios activos
            "status": "active"
        }
    },
    {
        "$sort": {  # Ordenar por fecha de creación
            "created_at": -1
        }
    },
    {
        "$limit": 100  # Limitar el número de resultados
    }
]

# Ejecutar la consulta
result = list(collection.aggregate(pipeline))

# Guardar resultado en JSON
json_file_path = "resultado_mongo.json"
with open(json_file_path, 'w') as json_file:
    json.dump(result, json_file, default=str)

# Subir a HDFS
hdfs = PyWebHdfsClient(host='localhost', port='9870', user_name='root')
with open(json_file_path, 'r') as file:
    content = file.read()

hdfs.create_file("/data/raw/resultado_mongo.json", content)
print("Resultado de MongoDB subido a HDFS en formato JSON")

# ----------

# ---------- MYSQL ----------

import mysql.connector
import json
from pywebhdfs.webhdfs import PyWebHdfsClient

# Conexión a MySQL
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='my-secret-pw',
    port=3306,
    database='transporte',  # Cambia esto por el nombre de tu base de datos
    auth_plugin='mysql_native_password'  # 🔹 Esto evita problemas de autenticación
)

# Consulta MySQL
query = "SELECT * FROM users"  # Asegúrate de que la tabla sea correcta
cursor = connection.cursor()
cursor.execute(query)
result = cursor.fetchall()

# Guardar resultado en TXT
txt_file_path = "resultado_mysql.txt"
with open(txt_file_path, 'w') as txt_file:
    for row in result:
        txt_file.write(str(row) + '\n')

# Subir a HDFS
hdfs = PyWebHdfsClient(host='localhost', port='9870', user_name='root')
with open(txt_file_path, 'r') as file:
    content = file.read()

hdfs.create_file("/data/raw/resultado_mysql.txt", content)
print("Resultado de MySQL subido a HDFS en formato TXT")

# Cerrar conexión
cursor.close()
connection.close()


# ----------


# ---------- NEO4J ----------

from neo4j import GraphDatabase
import csv
from pywebhdfs.webhdfs import PyWebHdfsClient

# Conexión a Neo4j
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "my-secret-pw"))  # Autenticación con tu contraseña

# Consulta Neo4j
query = "MATCH (p:Person) RETURN p.name, p.age"  # Cambia por tu consulta
with driver.session() as session:
    result = session.run(query)
    records = result.data()

# Guardar resultado en CSV
csv_file_path = "resultado_neo4j.csv"
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["name", "age"])
    for record in records:
        writer.writerow([record['p.name'], record['p.age']])

# Subir a HDFS
hdfs = PyWebHdfsClient(host='localhost', port='9870', user_name='root')
with open(csv_file_path, 'r') as file:
    content = file.read()

hdfs.create_file("/data/raw/resultado_neo4j.csv", content)
print("Resultado de Neo4j subido a HDFS en formato CSV")


# ----------


