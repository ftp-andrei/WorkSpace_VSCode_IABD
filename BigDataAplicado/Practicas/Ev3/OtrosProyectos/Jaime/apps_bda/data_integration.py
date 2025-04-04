# Ajustar la lectura y escritura para manejar mejor los encabezados y la codificación

from pyspark.sql import SparkSession

# Configuración del SparkSession
aws_access_key_id = 'test'
aws_secret_access_key = 'test'

spark = SparkSession.builder \
    .appName("SPARK S3") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
    .config("spark.sql.shuffle.partitions", "4") \
    .config("spark.jars.packages","org.apache.spark:spark-hadoop-cloud_2.13:3.5.1,software.amazon.awssdk:s3:2.25.11") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.driver.extraClassPath", "/opt/spark/jars/s3-2.25.11.jar") \
    .config("spark.executor.extraClassPath", "/opt/spark/jars/s3-2.25.11.jar") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

df3 = spark.read.option("delimiter", ",") \
    .option("header", "true") \
    .option("encoding", "UTF-8") \
    .csv("../spark-data/csv/ceseuve.csv")

df3.show()

df3.write \
    .option('fs.s3a.committer.name', 'partitioned') \
    .option('fs.s3a.committer.staging.conflict-mode', 'replace') \
    .option("fs.s3a.fast.upload.buffer", "bytebuffer") \
    .option("header", "true") \
    .mode('overwrite') \
    .csv(path='s3a://cubito/output', sep=',')

df3 = spark.read.option("delimiter", ",") \
    .option("encoding", "UTF-8") \
    .csv("../spark-data/json/tablapostgres/*")

df3.show()

df3.write \
    .option('fs.s3a.committer.name', 'partitioned') \
    .option('fs.s3a.committer.staging.conflict-mode', 'replace') \
    .option("fs.s3a.fast.upload.buffer", "bytebuffer") \
    .mode('overwrite') \
    .csv(path='s3a://cubito/basededatos', sep=',')


spark.stop()
