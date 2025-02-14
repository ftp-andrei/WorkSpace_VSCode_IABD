# pip install PyWebHdfs py2neo pymongo mysql-connector-python

from pywebhdfs.webhdfs import PyWebHdfsClient
from pymongo import MongoClient
import json

# Cliente de HDFS
hdfs_client = PyWebHdfsClient(host='localhost', port='9870', user_name='root') # 9870 en lugar de 50070

# Conexión a MongoDB
client = MongoClient("mongodb://mongoadmin:secret@localhost:27017/")
db = client["PokemonDB"]
collection = db["empleados"]

# Exportar documentos a un archivo JSON
with open("mongo_empleados.json", "w") as jsonfile:
    data = list(collection.find({}, {"_id": 0}))  # Excluye el campo _id
    json.dump(data, jsonfile, indent=4)

# Subir el archivo JSON a HDFS
with open("mongo_empleados.json", "rb") as f:
    hdfs_client.create_file('/data/mongo/empleados.json', f.read(), overwrite=True)
