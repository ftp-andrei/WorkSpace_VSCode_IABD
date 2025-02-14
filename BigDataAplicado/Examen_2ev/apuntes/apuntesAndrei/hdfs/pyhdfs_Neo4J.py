# pip install PyWebHdfs py2neo pymongo mysql-connector-python

from pywebhdfs.webhdfs import PyWebHdfsClient
import csv
from py2neo import Graph
from neo4j import GraphDatabase
# Cliente de HDFS
hdfs_client = PyWebHdfsClient(host='localhost', port='9870', user_name='root') # 9870 en lugar de 50070

# Conexión a Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "my-secret-pw"))
# Con GraphDatabase
# graph = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "my-secret-pw"))

# Ejecutar consulta y exportar resultados a CSV
query = """
MATCH (n:Empleado)
RETURN n.id AS id, n.nombre AS nombre, n.edad AS edad, n.departamento AS departamento, n.salario AS salario
"""
results = graph.run(query)

with open("neo4j_empleados.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(results.keys())  # Escribe los encabezados
    writer.writerows(results)

# Subir el archivo CSV exportado a HDFS
with open("neo4j_empleados.csv", "rb") as f:
    hdfs_client.create_file('/data/neo4j/empleados.csv', f.read(), overwrite=True)
