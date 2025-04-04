from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, when, to_date, weekofyear, month

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
    .appName("ANALISIS TEMPORAL") \
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



df_date = df_joined.withColumn('date_only', to_date(col(date)))
df_date = df_date.groupBy("date_only").agg(
    sum(revenue).alias("total_revenue"),
    sum(quantity).alias("total_quantity_sold")
)

df_week = df_joined.withColumn('week_of_year', weekofyear(col(date)))
df_week = df_week.groupBy("week_of_year").agg(
    sum(revenue).alias("total_revenue"),
    sum(quantity).alias("total_quantity_sold")
)
df_month = df_joined.withColumn('month', month(col(date)))
df_month = df_month.groupBy("month").agg(
    sum(revenue).alias("total_revenue"),
    sum(quantity).alias("total_quantity_sold")
)
df_season= df_joined.withColumn(
                    "season",
                    when((month(date) >= 3) & (month(date) <= 5), "Primavera")
                    .when((month(date) >= 6) & (month(date) <= 8), "Verano")
                    .when((month(date) >= 9) & (month(date) <= 11), "Otoño")
                    .otherwise("Invierno")
                )

df_season = df_season.groupBy("season").agg(
    sum(revenue).alias("total_revenue"),
    sum(quantity).alias("total_quantity_sold")
)

print('\n Agrupacion por dias: \n')

df_date.show()

print('Agrupacion por semanas: \n')

df_week.show()

print('Agrupacion por meses: \n')

df_month.show()

print('Ventas en fecha exacta: \n')

df_season.show()