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
    StructField("OrderID", IntegerType(), True),
    StructField("StoreID", IntegerType(), True),
    StructField("ProductID", StringType(), True),
    StructField("Revenue", FloatType(), True),
    StructField("Date", StringType(), True),
])

df_csv = spark.read.csv("s3a://cubito/output/*.csv", header=True, inferSchema=True)

from pyspark.sql.functions import col, avg, when

# Revenue

df_csv_mean_reve = df_csv.withColumn("Revenue", col("Revenue").cast("float"))
mean_revenue = df_csv_mean_reve.select(avg("Revenue")).first()[0]

df_csv = df_csv_mean_reve.fillna({"Revenue": round(mean_revenue, 2)})

# Quantity

df_csv_mean_quan = df_csv.withColumn("Quantity Sold", col("Quantity Sold").cast("float"))

mean_quantity = df_csv_mean_quan.select(avg("Quantity Sold")).first()[0]
df_csv = df_csv_mean_quan.fillna({"Quantity Sold": round(mean_quantity, 2)})

# Store

df_csv_store = df_csv.withColumn("Store ID", col("Store ID").cast("int"))

df_csv = df_csv_store.dropna(subset=["Store ID"])

# Product

df_csv_prod = df_csv.filter(~col("Product ID").cast("string").startswith("#"))

df_csv = df_csv_prod.dropna(subset=["Product ID"])

# Date

df_csv_mean_date = df_csv.withColumn("Date", col("Date").cast("Date"))
df_csv_mean_date = df_csv_mean_date.dropna(subset=["Date"])
mode_date = df_csv_mean_date.groupBy("Date").count().orderBy(col("count").desc()).first()[0]

mode_date_str = mode_date.strftime('%Y-%m-%d')

df_csv = df_csv_mean_date.fillna({"Date": mode_date_str})


df_csv.show(50)

#df_csv.write.csv("s3://cubito/processed_ceseuve.csv", header=True)