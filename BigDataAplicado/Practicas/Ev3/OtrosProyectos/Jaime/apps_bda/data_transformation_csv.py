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
    StructField("_c2", StringType(), True),
    StructField("_c1", IntegerType(), True),
    StructField("_c3", IntegerType(), True),
    StructField("_c4", FloatType(), True),
    StructField("_c0", StringType(), True),
])

df_csv = spark.read.csv("s3a://cubito/output/*.csv", header=False, inferSchema=True)

from pyspark.sql.functions import col, avg, when, to_date

# Duplicados

df_csv = df_csv.dropDuplicates()

# Nuevas cols

df_csv = df_csv.withColumn(
    "Tratado",
    when(
        col("_c4").isNull() | col("_c4").cast("float").isNull() |
        col("_c3").isNull() | col("_c3").cast("float").isNull() |
        col("_c0").isNull() | to_date(col("_c0"), "yyyy-MM-dd").isNull(),
        "Sí"
    ).otherwise("No")
)

df_csv = df_csv.withColumn("Fecha Inserción", current_timestamp())
    
# _c4

df_csv_mean_reve = df_csv.withColumn("_c4", col("_c4").cast("float"))
mean__c4 = df_csv_mean_reve.select(avg("_c4")).first()[0]

df_csv = df_csv_mean_reve.fillna({"_c4": round(mean__c4, 2)})

# _c3

df_csv_mean_quan = df_csv.withColumn("_c3", col("_c3").cast("float"))

mean_quantity = df_csv_mean_quan.select(avg("_c3")).first()[0]
df_csv = df_csv_mean_quan.fillna({"_c3": round(mean_quantity, 2)})

# Cuartiles de _c3

q1, q3 = df_csv.approxQuantile("_c3", [0.25, 0.75], 0.05)
iqr = q3 - q1

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

df_csv_clean = df_csv.filter((col("_c3") >= lower_bound) & (col("_c3") <= upper_bound))

# Store

df_csv_store = df_csv.withColumn("_c1", col("_c1").cast("int"))

df_csv = df_csv_store.dropna(subset=["_c1"])

# Product

df_csv_prod = df_csv.filter(~col("_c2").cast("string").startswith("#"))

df_csv = df_csv_prod.dropna(subset=["_c2"])

# Date

df_csv_mean_date = df_csv.withColumn("_c0", col("_c0").cast("Date"))
df_csv_mean_date = df_csv_mean_date.dropna(subset=["_c0"])
mode_date = df_csv_mean_date.groupBy("_c0").count().orderBy(col("count").desc()).first()[0]

mode_date_str = mode_date.strftime('%Y-%m-%d')

df_csv = df_csv_mean_date.fillna({"_c0": mode_date_str})

df_csv.show(50)

df_csv.write.mode("append").csv("s3a://cubito/processed/datos_compra", header=True)
