from pyspark.sql import SparkSession
# DataFrame cargado desde MySQL/PostgreSQL
# Se asume que el DataFrame tiene las columnas "store_id" y "monto"
# Configuración de Spark
spark = SparkSession.builder \
    .appName("SQL to S3") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
    .config("spark.hadoop.fs.s3a.access.key", "test") \
    .config("spark.hadoop.fs.s3a.secret.key", "test") \
    .config("spark.sql.shuffle.partitions", "4") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Configuración de conexión a MySQL/PostgreSQL
db_url = "jdbc:mysql://mysql:3306/retail-db"
properties = {"user": "root", "password": "root", "driver": "com.mysql.cj.jdbc.Driver"}

# Leer datos de la tabla "ventas"
df_ventas = spark.read.jdbc(db_url, "ventas", properties=properties)

# Seleccionar columnas específicas (por ejemplo, "store_id", "monto")
df_seleccionado = df_ventas.select("store_id", "monto")

# Mostrar el DataFrame resultante
df_seleccionado.show()

# Guardar en S3
df_seleccionado.write.mode('overwrite').csv('s3a://bucket/sql_data', header=True, sep=',')

spark.stop()
