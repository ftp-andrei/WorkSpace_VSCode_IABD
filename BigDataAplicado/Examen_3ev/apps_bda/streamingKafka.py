from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType

aws_access_key_id='test'
aws_secret_access_key='test'

spark = SparkSession.builder \
    .appName("Streaming from Kafka") \
    .config("spark.streaming.stopGracefullyOnShutdown", True) \
    .config("spark.sql.shuffle.partitions", 4) \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
    .config("spark.jars.packages","org.apache.spark:spark-hadoop-cloud_2.13:3.5.1,software.amazon.awssdk:s3:2.25.11,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.driver.extraClassPath", "/opt/spark/jars/s3-2.25.11.jar") \
    .config("spark.executor.extraClassPath", "/opt/spark/jars/s3-2.25.11.jar") \
    .master("spark://spark-master:7077") \
    .getOrCreate()
    
df =spark  \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:9093") \
  .option("subscribe", "sales_stream") \
  .load()

schema = StructType() \
    .add("timestamp", IntegerType()) \
    .add("evento", StringType()) \
    .add("nombre", StringType()) \
    .add("equipo", StringType()) \
    .add("resultado", DoubleType())

df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")

df.printSchema()

query = df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()
# cambiar formato y bucket si fuese necesario
query = df \
    .writeStream \
    .outputMode("append") \
    .format("json") \
    .option("path", "s3a://bucket/outputKafka") \
    .option("checkpointLocation", "s3a://bucket/checkopoint")\
    .option("header", "true")\
    .start()

query.awaitTermination()