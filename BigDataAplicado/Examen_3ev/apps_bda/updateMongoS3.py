from pyspark.sql import SparkSession
import pymongo
from pymongo import MongoClient


aws_access_key_id = 'test'
aws_secret_access_key = 'test'

try:
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
    
    #mongo_client = pymongo.MongoClient("mongodb://mongoadmin:secret@localhost:7777/")
    mongo_client = MongoClient("mongodb://mongoadmin:secret@localhost:7777/")
    db = mongo_client["pokemon_events_db"]  

    events_collection = db["events_collection"]

    dataEvents=events_collection.find({},{'_id': False})

    dfMongo=spark.createDataFrame(dataEvents)
    
    dfMongo \
    .write \
    .option('fs.s3a.committer.name', 'partitioned') \
    .option('fs.s3a.committer.staging.conflict-mode', 'replace') \
    .option("fs.s3a.fast.upload.buffer", "bytebuffer")\
    .mode('overwrite') \
    .json(path='s3a://bucket/pokemon_events-json')
    
    spark.stop()
    
except Exception as e:
    print(e)
    
    
