from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

aws_access_key_id = 'test'
aws_secret_access_key = 'test'

# Crear sesión de Spark
spark = SparkSession.builder \
    .appName("csvTransformData") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
    .config("spark.sql.shuffle.partitions", "4") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Definir esquema explícito
schema = StructType([
    StructField("Date", IntegerType(), True),
    StructField("Evento", StringType(), True),
    StructField("Nombre", StringType(), True),
    StructField("Equipo", StringType(), True),
    StructField("Resultado", FloatType(), True),
])

# Leer CSV desde S3 usando LocalStack con esquema definido
df_csv = spark.read.csv("s3a://bucket/sales_compacted_csv/*.csv", header=True, schema=schema)
# --------------------
# Limpieza de datos
# --------------------

# 1️⃣ Resultado: Reemplazar valores nulos por la media
mean_Resultado = df_csv.select(avg("Resultado")).first()[0]
df_csv = df_csv.fillna({"Resultado": round(mean_Resultado, 2)})

# 2️⃣ Equipo: Asegurar tipo y reemplazar nulos por la media
mean_quantity = df_csv.select(avg("Equipo")).first()[0]
df_csv = df_csv.fillna({"Equipo": int(round(mean_quantity))})

# 3️⃣ Evento: Eliminar registros con `Evento` nulo
df_csv = df_csv.dropna(subset=["Evento"])

# 4️⃣ Nombre: Filtrar productos que comiencen con `#` y eliminar nulos
df_csv = df_csv.filter((col("Nombre").isNotNull()) & (~col("Nombre").startswith("#")))

# --------------------
# Guardar los datos en S3 (LocalStack) en formato Parquet
# --------------------
output_path = "s3a://bucket/output/processed_data_csv.parquet"
df_csv.write.mode("overwrite").parquet(output_path)

print("Transformación completada y datos guardados correctamente.")
