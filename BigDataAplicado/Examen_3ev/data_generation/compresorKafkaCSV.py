from pyspark.sql import SparkSession

aws_access_key_id = 'test'
aws_secret_access_key = 'test'

try:
    spark = SparkSession.builder \
        .appName("Streaming from Kafka") \
        .config("spark.streaming.stopGracefullyOnShutdown", True) \
        .config("spark.sql.shuffle.partitions", 4) \
        .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
        .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
        .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
        .config("spark.jars.packages", "org.apache.spark:spark-hadoop-cloud_2.13:3.5.1,software.amazon.awssdk:s3:2.25.11,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.driver.extraClassPath", "/opt/spark/jars/s3-2.25.11.jar") \
        .config("spark.executor.extraClassPath", "/opt/spark/jars/s3-2.25.11.jar") \
        .master("spark://spark-master:7077") \
        .getOrCreate()
    
    spark.conf.set("spark.hadoop.fs.s3a.connection.maximum", "100")
    spark.conf.set("spark.hadoop.fs.s3a.fast.upload", "true")
    spark.conf.set("spark.hadoop.fs.s3a.path.style.access", "true")
    spark.conf.set("spark.hadoop.fs.s3a.committer.name", "partitioned")

    # Ruta a los archivos CSV en S3
    source_path = "s3a://bucket/outputKafka/*.csv"  # Carga todos los CSV del bucket
    
    # Leer múltiples archivos CSV desde S3
    df = spark.read.option('header', 'true').option("delimiter", ",").csv(source_path)

    # Realizar cualquier procesamiento si es necesario
    df.show(5)  # Muestra los primeros 5 registros para verificar la lectura

    # Guardar el archivo en formato JSON en S3
    df.coalesce(1).write.mode("overwrite").csv("s3a://bucket/sales_compacted_csv")

    print("Datos comprimidos con éxito.")
except Exception as e:
    print("Error reading data from S3:", e)    
finally:
    spark.stop()
