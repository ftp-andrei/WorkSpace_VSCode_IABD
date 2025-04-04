docker compose build
docker compose up -d
-----

docker exec -it {nombreSpark} /bin/bash
spark-master, una vez dentro ir a ../spark-apps y luego ejecutar
python {nombreArchivo.py}
test_clust.py


redshift no entra en examen
kafka si
--------------------
subir a s3 los 2 archivos de json
el mongo subirlo a mongo, y bajarlo en .json/csv 
subirlo a s3 

Kafka igual que en la practica





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






----------------------------------------




-----------------------
LOCALSTACK
-----------------------
# Si hay un SparkSession no se ejcuta
docker exec -it localstack /bin/bash

-- Crear bucket 
awslocal s3api create-bucket --bucket sample-bucket 

-- Ver buckets 
awslocal s3api list-buckets 

-- Crear objeto 
awslocal s3api put-object --bucket sample-bucket --key image.jpg --body image.jpg

-- Ver contenido 
aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
aws configure set region us-east-1


aws --endpoint-url=http://localhost:4566 s3 ls s3://bucket/output/


-- Como conectarse a S3:

dentro de sparkS3.py 
Nos faltará una ip: 4566
Endpoint: http://localstack:4566
Si quiero ejecutar un job, poner el key id y el access key de aws 
El sdk y la dependencia a file system


Como podemos comprobar si un nombre de dominio funciona: hacer ping

-- Para subir archivo a S3 
Mas abajo meter en el read (en el try) de s3 poner un .csv que exista dentro de apps

Si no es un .csv se cambiaria el final (.csv) al formato que es el archivo


-----------------------
POSTGRES
-----------------------

docker exec -it postgres-db /bin/bash 

psql -U postgres -d retail_db -c 'SELECT * FROM Stores limit 10'

#Nos metemos a sparkmaster
python read_database.py 
(posible error, cambiar url de jdbc a postgres_db)






-----------------------
KAFKA
-----------------------
# Ejecutamos para q produzca
python kafka_producer.py
# Ejecutando esto lo veriamos
python kafka_consumer.py 

# Para generar datos en kafka, hace falta unos datos (json (?)) y el schema
# Ejecutamos el streamingkafka desde el master (desde apps)
python streamingkafka.py

# Si vamos a localstack y entramos dentro del bucket veremos el /sales

