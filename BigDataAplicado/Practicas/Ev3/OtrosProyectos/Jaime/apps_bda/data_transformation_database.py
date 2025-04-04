from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
aws_access_key_id = 'test'
aws_secret_access_key = 'test'

spark = SparkSession.builder \
    .appName("csvTransformData") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
    .config("spark.sql.shuffle.partitions", "4") \
    .config("spark.jars.packages","org.apache.hadoop:hadoop-aws:3.3.4") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

schema = StructType([
    StructField("_c0", IntegerType(), True),
    StructField("_c1", StringType(), True),
    StructField("_c2", StringType(), True),
    StructField("_c3", StringType(), True),
])

df_csv = spark.read.csv("s3a://cubito/basededatos/*.csv", header=True, inferSchema=True)

from pyspark.sql.functions import col, avg, when, to_date

# Duplicados

df_csv = df_csv.dropDuplicates()

# Nuevas cols

df_csv = df_csv.withColumn(
    "Tratado",
    when(
        col("_c1").isNull() | col("_c1").startswith("#") |
        col("_c2").isNull() | col("_c2").startswith("#") |
        col("_c3").isNull() | col("_c3").startswith("#"),
        "Sí"
    ).otherwise("No")
)

df_csv = df_csv.withColumn("Fecha Inserción", current_timestamp())
    
# _c1

df_csv = df_csv.withColumn(
    "_c1", 
    when(
        col("_c1").cast("string").startswith("#"), 
        None
    ).otherwise(col("_c1"))
)

df_csv = df_csv.fillna({"_c1": "Sin especificar"})


# _c2

df_csv = df_csv.withColumn(
    "_c2", 
    when(
        col("_c2").cast("string").startswith("#"), 
        None
    ).otherwise(col("_c2"))
)

df_csv = df_csv.fillna({"_c2": "Sin especificar"})

# _c3

df_csv = df_csv.withColumn(
    "_c3", 
    when(
        col("_c3").cast("string").startswith("#"), 
        None
    ).otherwise(col("_c3"))
)

df_csv = df_csv.fillna({"_c3": "Sin especificar"})



df_csv.show(50)

df_csv.write.mode("append").csv("s3a://cubito/processed/datos_tienda", header=True)
