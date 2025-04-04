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
    StructField("timestamp", StringType(), True),
    StructField("store_id", IntegerType(), True),
    StructField("product_id", StringType(), True),
    StructField("quantity_sold", IntegerType(), True),
    StructField("revenue", FloatType(), True),
])

# Leer JSON desde S3 usando LocalStack con esquema definido
df_json = spark.read.json("s3a://bucket/sales_compacted_json/*.json", schema=schema)
df_json.show(10)
# --------------------
# Limpieza de datos
# --------------------

# 1️⃣ Revenue: Reemplazar valores nulos por la media
mean_revenue_row = df_json.select(avg("revenue")).first()
mean_revenue = mean_revenue_row[0] if mean_revenue_row[0] is not None else 0.0  # Evita error NoneType
df_json = df_json.fillna({"revenue": round(mean_revenue, 2)})

# 2️⃣ Quantity Sold: Asegurar tipo y reemplazar nulos por la media
mean_quantity_row = df_json.select(avg("quantity_sold")).first()
mean_quantity = int(round(mean_quantity_row[0])) if mean_quantity_row[0] is not None else 1  # Evita error NoneType
df_json = df_json.fillna({"quantity_sold": mean_quantity})

# 3️⃣ Store ID: Eliminar registros con `store_id` nulo
df_json = df_json.dropna(subset=["store_id"])

# 4️⃣ Product ID: Filtrar productos que comiencen con `#` y eliminar nulos
df_json = df_json.filter((col("product_id").isNotNull()) & (~col("product_id").startswith("#")))

# 5️⃣ Date: Reemplazar valores nulos con la moda (timestamp más frecuente)
df_json = df_json.dropna(subset=["timestamp"])
mode_timestamp_row = df_json.groupBy("timestamp").count().orderBy(col("count").desc()).first()
mode_timestamp = mode_timestamp_row[0] if mode_timestamp_row is not None else "1970-01-01"  # Valor por defecto
df_json = df_json.fillna({"timestamp": mode_timestamp})

# --------------------
# Guardar los datos en S3 (LocalStack) en formato Parquet
# --------------------
output_path = "s3a://bucket/output/processed_data_json.parquet"
df_json.write.mode("overwrite").json(output_path)

# Mostrar resultado
df_json.printSchema()
df_json.show(10)

print("Transformación completada y datos guardados correctamente.")
