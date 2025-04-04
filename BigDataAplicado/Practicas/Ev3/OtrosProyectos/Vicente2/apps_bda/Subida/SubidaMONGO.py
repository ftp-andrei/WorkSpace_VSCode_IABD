from pyspark.sql import SparkSession

# Configuración de acceso a S3 (LocalStack)
aws_access_key_id = 'test'
aws_secret_access_key = 'test'

# Configuración de Spark y conexión con MongoDB
spark = SparkSession.builder \
    .appName("MongoDB to S3") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
    .config("spark.sql.shuffle.partitions", "4") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Definir URI de conexión a MongoDB
mongo_uri = "mongodb://root:contraseñaroot@mongo:27017/retail-db"

# Leer la colección "tienda" desde MongoDB
# Se asume que "tienda" contiene información sobre tiendas

df_tienda = spark.read.format("mongo").option("uri", f"{mongo_uri}.tienda").load()

# Leer la colección "ventas" desde MongoDB
# Se asume que "ventas" contiene registros de ventas asociadas a tiendas

df_ventas = spark.read.format("mongo").option("uri", f"{mongo_uri}.ventas").load()

# Realizar un INNER JOIN entre "tienda" y "ventas" usando store_id como clave
# Se asume que ambas colecciones tienen la columna "store_id" para hacer la relación

df_joined = df_tienda.join(df_ventas, df_tienda["store_id"] == df_ventas["store_id"], "inner")

# Si no es necesario hacer el JOIN, simplemente se puede trabajar con "df_tienda"
# df_joined = df_tienda  # Descomentar esta línea si solo se necesita "tienda"

# Guardar el DataFrame resultante en un bucket S3 simulado en LocalStack
# Se almacena como CSV con encabezado y separador de coma

df_joined.write.mode('overwrite').csv('s3a://bucket/mongo_data', header=True, sep=',')

# Finalizar la sesión de Spark
spark.stop()