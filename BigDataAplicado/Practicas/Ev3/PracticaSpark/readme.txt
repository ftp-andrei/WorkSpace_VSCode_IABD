docker compose build
docker compose up -d
-----

docker exec -it {nombreSpark} /bin/bash
spark-master, una vez dentro ir a ../spark-apps y luego ejecutar
python {nombreArchivo.py}
test_clust.py


redshift no entra en examen
kafka si



------------
PRACTICA PASO A PASO
------------

-- Crear bucket desde local 
python createBucket.py

-- Ejecutar para crear el csv en local 
python csvData.py

-- Nos metemos al master y lo subo al bucket ( .csv().toDF )
docker exec -it spark-master /bin/bash
cd ..
cd ..
python opt/spark-apps/data_integration.py

-- Despues nos metemos al localstack y comprobar que esta subido 
docker exec -it localstack /bin/bash
    OPCION 1: awslocal s3 ls s3://bucket/  
    OPCION 2: awslocal s3api list-objects --bucket bucket


-----
DATABASE
-----
-- Ejecutamos para generar la bd y los datos desde local 
python databaseData.py

-- Nos metemos a postgres y vemos si estan los datos
docker exec -it postgres-db /bin/bash
psql -U postgres -d retail_db

\dt -> ver las tablas 
\d {nombreTabla} -> ver columnas y los tipos

-- Ejecutamos para ver que existen los datos
SELECT * FROM stores LIMIT 10;

DROP TABLE stores;

#### 
CREAR CSV CON LA BD Y SUBIR AL BUCKET (subirCsv.py)
####

-----
KAFKA
-----
-- Ejecutar en local el kafka-producer y en el master el streamingKafka
LOCAL: python kafka_producer.py 
docker exec -it spark-master /bin/bash
(Desde /)
MASTER: python opt/spark-apps/streamingKafka.py

####
QUE SEA JSON EN VEZ DE CSV
####

Juntar los parts usando el compresorKafka.py desde master y aplicar tratamiento de datos


-----
TRANSFORMACIÓN DE DATOS 
-----

------- TRATAMIENTO DE LOS VALORES -------

-- Ejecutamos desde el spark-master el valorPerdido.py
python opt/spark-apps/valorPerdido.py

-- Verificamos que esta subido al bucket
    OPCION 1: awslocal s3 ls s3://bucket/  
    OPCION 2: awslocal s3api list-objects --bucket bucket

(
para visualizar los datos 
    df.printSchema()
    df.show(50)
)





