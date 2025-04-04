from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, when, split, expr, desc

aws_access_key_id = 'test'
aws_secret_access_key = 'test'

date= 'date'
stores= 'store_ID'
name= 'store_name'
location= 'location'
demographics= 'demographics'
products= 'product_ID'
quantity= 'quantity_Sold'
revenue= 'revenue'
tratado= 'Tratado'
fecha_insercion= 'fecha_Insercion'

spark = SparkSession.builder \
    .appName("ANALISIS GEOGRAFICO") \
    .config("spark.driver.extraClassPath", "/opt/spark-apps/drivers/postgresql-42.7.3.jar:/opt/spark/jars/*") \
    .config("spark.executor.extraClassPath", "/opt/spark-apps/drivers/postgresql-42.7.3.jar:/opt/spark/jars/*") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

jdbc_url = "jdbc:postgresql://postgres-db:5432/processed_data"
connection_properties = {
    "user": "postgres",
    "password": "casa1234",
    "driver": "org.postgresql.Driver"
}

table_csv = "csv_data"
df_csv = spark.read.jdbc(url=jdbc_url, table=table_csv, properties=connection_properties)

table_csv = "postgre_data"
df_db = spark.read.jdbc(url=jdbc_url, table=table_csv, properties=connection_properties)

table_csv = "kafka_data"
df_kafka = spark.read.jdbc(url=jdbc_url, table=table_csv, properties=connection_properties)

# Renombrar columnas en df_csv y df_kafka para que coincidan
df_csv = df_csv.withColumnRenamed("date", date) \
             .withColumnRenamed("store_ID", stores) \
             .withColumnRenamed("product_ID", products) \
             .withColumnRenamed("quantity_Sold", quantity) \
             .withColumnRenamed("revenue", revenue) \
             .withColumnRenamed("Tratado", tratado) \
             .withColumnRenamed("Fecha Insercion", fecha_insercion)

df_kafka = df_kafka.withColumnRenamed("timestamp", date) \
                 .withColumnRenamed("store_id", stores) \
                 .withColumnRenamed("product_id", products) \
                 .withColumnRenamed("quantity_sold", quantity) \
                 .withColumnRenamed("revenue", revenue) \
                 .withColumnRenamed("Tratado", tratado) \
                 .withColumnRenamed("Fecha Insercion", fecha_insercion)

# Seleccionar y ordenar columnas para que coincidan antes de la unión
columns_union = [date, stores, products, quantity, revenue, tratado, fecha_insercion]
df_csv = df_csv.select(columns_union)
df_kafka = df_kafka.select(columns_union)

df_union = df_csv.union(df_kafka)

df_joined = df_union.join(df_db, stores, "inner")

df_grouped = df_joined.groupBy(col(location)).agg(sum(col("revenue")).alias("total_revenue"))
df_grouped = df_grouped.orderBy(col("total_revenue").desc())
# max_revenue = df_grouped.agg(max(col("total_revenue"))).collect()[0][0]
# df_location_max = df_grouped.filter(col("total_revenue") == max_revenue)
# df_top_location = df_location_max.join(df_db, location, "inner")

# Extraer latitud y longitud correctamente
df_demographics = df_joined.withColumn("latitude", split(df_joined[demographics], ",")[0].substr(2, 1000)) \
                            .withColumn("longitude", split(df_joined[demographics], ",")[1].substr(0, 1000))

df_demographics = df_demographics.withColumn("longitude", expr("substring(longitude, 1, length(longitude) - 1)"))

df_continents = df_demographics.withColumn(
    "continent",
    when((col("latitude") >= 7) & (col("latitude") <= 83) & (col("longitude") >= -170) & (col("longitude") <= -50), "North America")
    .when((col("latitude") >= -55) & (col("latitude") <= 15) & (col("longitude") >= -90) & (col("longitude") <= -30), "South America")
    .when((col("latitude") >= 35) & (col("latitude") <= 71) & (col("longitude") >= -25) & (col("longitude") <= 60), "Europe")
    .when((col("latitude") >= -35) & (col("latitude") <= 37) & (col("longitude") >= -20) & (col("longitude") <= 55), "Africa")
    .when((col("latitude") >= 0) & (col("latitude") <= 77) & (col("longitude") >= 25) & (col("longitude") <= 180), "Asia")
    .when((col("latitude") >= -50) & (col("latitude") <= 10) & (col("longitude") >= 110) & (col("longitude") <= 180), "Oceania")
    .otherwise("Unknown")
)

df_filtered = df_continents.groupBy("continent").agg(sum("revenue").alias("total_revenue"))

print('\n Localización con mas beneficios de venta: \n')

df_grouped.show()

print('Ventas segun el continente: \n')

df_filtered.orderBy(desc("continent")).show()