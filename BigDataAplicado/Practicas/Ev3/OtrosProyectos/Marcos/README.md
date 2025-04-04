# ProyectoSpark
INSTRUCCIONES DE EJECUCION

INICIO DEL PROYECTO

1- Crear el cluster, primero vamos a la carpeta de Spark
Comandos:
docker compose build
docker compose up -d

2- Ejecutar los scripts del archivo src\scripts\posgresql_arregaldo.txt

3- Crear el bucket donde guardaremos los archivos
Comando: 
awslocal s3api create-bucket --bucket data-lake

EXTRACCION

4- Ejecutar los archivos src\extract\CSV\csvGeneration.py y src\extract\PostgreSQL\dbGeneration.py fuera del cluster

5- Ejecutamos los archivos src\extract\CSV\csvUpload.py y src\extract\PostgreSQL\dbUpload.py

6- Ejecutar el archivo src\extract\Kafka\kafkaGeneration.py y a la vez src\extract\Kafka\kafkaUpload.py para obtener la informacion de kafka, una vez se quiera apagar el envio de datos, se para primero el archvo src\extract\Kafka\kafkaGeneration.py y luego el archivo src\extract\Kafka\kafkaUpload.py

7- Para tener solo un archivo en el s3, ejecutamos el archivo src\extract\Kafka\compresorKafka.py

TRANSFORMACION

8- Creamos en postgres una nueva base de datos
Comandos: 
psql -h localhost -U postgres -d retail_db
CREATE DATABASE processed_data;

9- Ejecutamos los archivos src\transform\CSV\csvProcessing.py, src\transform\Kafka\kafkaProcessing.py, src\transform\PostgreSQL\dbProcessing.py

CARGA Y ANALISIS

10- Ejecutamos los archivos src\load\Queries\analisis_demográfico.py, src\load\Queries\analisis_geografico.py, src\load\Queries\analisis_temporal.py, src\load\Queries\analisis_ventas.py

FIN DEL PROYECTO