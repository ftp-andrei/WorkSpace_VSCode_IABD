from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

aws_access_key_id = 'test'
aws_secret_access_key = 'test'

# Crear sesión de Spark
spark = SparkSession.builder \
    .appName("jsonTransformData") \
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

# Leer JSON desde S3 usando LocalStack con esquema definido
df_json = spark.read.json("s3a://bucket/sales_compacted_json/*.json", schema=schema)

# --------------------
# Limpieza de datos
# --------------------

# 1️⃣ Resultado: Reemplazar valores nulos por la media
mean_Resultado_row = df_json.select(avg("Resultado")).first()
mean_Resultado = mean_Resultado_row[0] if mean_Resultado_row[0] is not None else 0.0  # Evita error NoneType
df_json = df_json.fillna({"Resultado": round(mean_Resultado, 2)})

# 2️⃣ Quantity Sold: Asegurar tipo y reemplazar nulos por la media
mean_quantity_row = df_json.select(avg("Equipo")).first()
mean_quantity = int(round(mean_quantity_row[0])) if mean_quantity_row[0] is not None else 1  # Evita error NoneType
df_json = df_json.fillna({"Equipo": mean_quantity})

# 3️⃣ Store ID: Eliminar registros con `Evento` nulo
df_json = df_json.dropna(subset=["Evento"])

# 4️⃣ Product ID: Filtrar productos que comiencen con `#` y eliminar nulos
df_json = df_json.filter((col("Nombre").isNotNull()) & (~col("Nombre").startswith("#")))


# --------------------
# Guardar los datos en S3 (LocalStack) en formato Parquet
# --------------------
output_path = "s3a://bucket/output/processed_data_json.parquet"
df_json.write.mode("overwrite").json(output_path)

print("Transformación completada y datos guardados correctamente.")
