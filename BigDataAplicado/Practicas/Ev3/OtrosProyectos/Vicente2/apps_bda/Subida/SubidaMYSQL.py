from pyspark.sql import SparkSession

# Configuración de acceso a S3 (LocalStack)
aws_access_key_id = 'test'
aws_secret_access_key = 'test'

# Configuración de Spark y conexión con MySQL
spark = SparkSession.builder \
    .appName("MySQL to S3") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
    .config("spark.sql.shuffle.partitions", "4") \
    .config("spark.jars", "/opt/spark/jars/mysql-connector-java-8.0.33.jar") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Definir la URL de conexión a MySQL y las propiedades de acceso
mysql_url = "jdbc:mysql://mysql:3306/retail-db"
properties = {"user": "root", "password": "root", "driver": "com.mysql.cj.jdbc.Driver"}

# Leer la tabla "tienda" desde MySQL
# Se asume que "tienda" contiene información sobre tiendas

df_tienda = spark.read.jdbc(mysql_url, "tienda", properties=properties)

# Leer la tabla "ventas" desde MySQL
# Se asume que "ventas" contiene registros de ventas asociadas a tiendas

df_ventas = spark.read.jdbc(mysql_url, "ventas", properties=properties)

# Realizar un INNER JOIN entre "tienda" y "ventas" usando store_id como clave
# Se asume que ambas tablas tienen la columna "store_id" para hacer la relación

df_joined = df_tienda.join(df_ventas, df_tienda["store_id"] == df_ventas["store_id"], "inner")

# Si no es necesario hacer el JOIN, simplemente se puede leer la tabla "ventas"
# df_joined = spark.read.jdbc(mysql_url, "ventas", properties=properties)  # Descomentar si solo se necesita "ventas"

# Guardar el DataFrame resultante en un bucket S3 simulado en LocalStack
# Se almacena como CSV con encabezado y separador de coma

df_joined.write.mode('overwrite').csv('s3a://bucket/mysql_data', header=True, sep=',')

# Finalizar la sesión de Spark
spark.stop()
