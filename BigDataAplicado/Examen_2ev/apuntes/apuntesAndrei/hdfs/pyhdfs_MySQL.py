# pip install PyWebHdfs py2neo pymongo mysql-connector-python

from pywebhdfs.webhdfs import PyWebHdfsClient
import mysql.connector
import csv
# Cliente de HDFS
hdfs_client = PyWebHdfsClient(host='localhost', port='9870', user_name='root') # 9870 en lugar de 50070

# Conexión a MySQL
conMySQL = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="your_database"
)
cursor = conMySQL.cursor()

# Exportar tabla a un archivo CSV
query = "SELECT * FROM empleados"
cursor.execute(query)

with open("empleados.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([i[0] for i in cursor.description])  # Escribe los encabezados
    writer.writerows(cursor.fetchall())

cursor.close()
conMySQL.close()

# Leer el archivo CSV y subirlo a HDFS
with open("empleados.csv", "rb") as f:
    hdfs_client.create_file('/data/mysql/empleados.csv', f.read(), overwrite=True)