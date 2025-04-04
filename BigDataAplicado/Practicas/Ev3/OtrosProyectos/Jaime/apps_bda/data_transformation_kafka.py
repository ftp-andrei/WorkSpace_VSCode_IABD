from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType
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

schema = StructType() \
    .add("timestamp", IntegerType()) \
    .add("store_id", IntegerType()) \
    .add("product_id", StringType()) \
    .add("quantity_sold", IntegerType()) \
    .add("revenue", DoubleType())

df_csv = spark.read.csv("s3a://cubito/output/*.csv", header=True, inferSchema=True)

from pyspark.sql.functions import col, avg, when

# Revenue

df_csv_mean_reve = df_csv.withColumn("revenue", col("revenue").cast("float"))
mean_revenue = df_csv_mean_reve.select(avg("revenue")).first()[0]

df_csv = df_csv_mean_reve.fillna({"revenue": round(mean_revenue, 2)})

# Quantity

df_csv_mean_quan = df_csv.withColumn("quantity_sold", col("quantity_sold").cast("int"))

mean_quantity = df_csv_mean_quan.select(avg("quantity_sold")).first()[0]
df_csv = df_csv_mean_quan.fillna({"quantity_sold": mean_quantity})

# Store

df_csv_store = df_csv.withColumn("store_id", col("store_id").cast("int"))

df_csv = df_csv_store.dropna(subset=["store_id"])

# Product

df_csv = df_csv.dropna(subset=["product_id"])

# Date

df_csv_mean_timestamp = df_csv.withColumn("timestamp", col("timestamp").cast("timestamp"))
df_csv_mean_timestamp = df_csv_mean_timestamp.dropna(subset=["timestamp"])
mode_timestamp = df_csv_mean_timestamp.groupBy("timestamp").count().orderBy(col("count").desc()).first()[0]

mode_timestamp_str = mode_timestamp.strftime('%Y-%m-%d')

df_csv = df_csv_mean_timestamp.fillna({"timestamp": mode_timestamp_str})


df_csv.show(50)

#df_csv.write.csv("s3://cubito/processed_ceseuve.csv", header=True)