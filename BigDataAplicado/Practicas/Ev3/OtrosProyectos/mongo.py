from pyspark.sql import SparkSession
# Si estás trabajando con MongoDB, puedes utilizar el parámetro select 
# al leer los datos para obtener solo las columnas que necesitas
# Configuración de Spark
spark = SparkSession.builder \
    .appName("MongoDB to S3") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
    .config("spark.hadoop.fs.s3a.access.key", "test") \
    .config("spark.hadoop.fs.s3a.secret.key", "test") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Conectar a MongoDB y leer la colección "ventas"
mongo_uri = "mongodb://root:root@mongo:27017/retail-db"

df_ventas = spark.read.format("mongo") \
    .option("uri", f"{mongo_uri}.ventas") \
    .load()

# Seleccionar columnas específicas (por ejemplo, "store_id", "monto")
df_seleccionado = df_ventas.select("store_id", "monto")

# Mostrar el DataFrame resultante
df_seleccionado.show()

# Guardar en S3
df_seleccionado.write.mode('overwrite').csv('s3a://bucket/mongo_data', header=True, sep=',')

spark.stop()
