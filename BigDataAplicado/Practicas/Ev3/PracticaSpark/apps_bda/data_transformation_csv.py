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
    StructField("Date", StringType(), True),
    StructField("Store ID", IntegerType(), True),
    StructField("Product ID", StringType(), True),
    StructField("Quantity Sold", IntegerType(), True),
    StructField("Revenue", FloatType(), True),
])

# Leer CSV desde S3 usando LocalStack con esquema definido
df_csv = spark.read.csv("s3a://bucket/outputKafka/*.csv", header=True, schema=schema)
df_csv.show(10)
# --------------------
# Limpieza de datos
# --------------------

# 1️⃣ Revenue: Reemplazar valores nulos por la media
mean_revenue = df_csv.select(avg("Revenue")).first()[0]
df_csv = df_csv.fillna({"Revenue": round(mean_revenue, 2)})

# 2️⃣ Quantity Sold: Asegurar tipo y reemplazar nulos por la media
mean_quantity = df_csv.select(avg("Quantity Sold")).first()[0]
df_csv = df_csv.fillna({"Quantity Sold": int(round(mean_quantity))})

# 3️⃣ Store ID: Eliminar registros con `Store ID` nulo
df_csv = df_csv.dropna(subset=["Store ID"])

# 4️⃣ Product ID: Filtrar productos que comiencen con `#` y eliminar nulos
df_csv = df_csv.filter((col("Product ID").isNotNull()) & (~col("Product ID").startswith("#")))

# 5️⃣ Date: Reemplazar valores nulos con la moda (fecha más frecuente)
df_csv = df_csv.dropna(subset=["Date"])
mode_date_row = df_csv.groupBy("Date").count().orderBy(col("count").desc()).first()

if mode_date_row:
    mode_date = mode_date_row[0]
    df_csv = df_csv.fillna({"Date": mode_date})
else:
    print("No se pudo calcular la moda para 'Date', no hay datos disponibles.")
    mode_date = None

# --------------------
# Guardar los datos en S3 (LocalStack) en formato Parquet
# --------------------
output_path = "s3a://bucket/output/processed_data_csv.parquet"
df_csv.write.mode("overwrite").parquet(output_path)

# Mostrar resultado
df_csv.printSchema()
df_csv.show(10)

print("Transformación completada y datos guardados correctamente.")
