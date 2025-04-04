from pyspark.sql import SparkSession

aws_access_key_id = 'test'
aws_secret_access_key = 'test'

spark = SparkSession.builder \
    .appName("SPARK S3 JSON to CSV") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
    .config("spark.sql.shuffle.partitions", "4") \
    .config("spark.jars.packages", "org.apache.spark:spark-hadoop-cloud_2.13:3.5.1,software.amazon.awssdk:s3:2.25.11") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.driver.extraClassPath", "/opt/spark/jars/s3-2.25.11.jar") \
    .config("spark.executor.extraClassPath", "/opt/spark/jars/s3-2.25.11.jar") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

try:
    df_json = spark.read.option("multiline", "true").json("/opt/spark-data/json/pokemon_data.json")  

    df_json2 = spark.read.option("multiline", "true").json("/opt/spark-data/json/pokemon_battle_events.json")  
    df_json \
        .write \
        .option("header", "true") \
        .mode("overwrite") \
        .json("s3a://bucket/pokemon_data-json")
    
    df_json2 \
        .write \
        .option("header", "true") \
        .mode("overwrite") \
        .json("s3a://bucket/pokemon_battle_events-json")
    
        # Leemos el TXT separado por tabuladores
    df_txt = spark.read.option("delimiter", "\t").option("header", "true").csv("/opt/spark-data/text/battle_records.txt")  
    
    # Lo escribimos en S3 como CSV con separador coma
    df_txt \
        .write \
        .option("header", "true") \
        .mode('overwrite') \
        .csv(path='s3a://bucket/battle_records-csv', sep=',')
    print("Archivos convertidos y escritos en S3 correctamente.")

    
except Exception as e:
    print("Error leyendo JSON")
    print(e)

finally:
    spark.stop()
