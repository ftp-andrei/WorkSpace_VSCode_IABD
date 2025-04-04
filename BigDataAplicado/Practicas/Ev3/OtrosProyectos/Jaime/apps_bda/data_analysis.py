from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, max, to_timestamp, lit

# Configuración de acceso a PostgreSQL
jdbc_url = "jdbc:postgresql://postgres-db:5432/retail_db"  # Asegúrate de que esta URL sea correcta
connection_properties = {
    "user": "postgres",
    "password": "casa1234",
    "driver": "org.postgresql.Driver"
}

# Inicializa Spark
spark = SparkSession.builder \
    .appName("ANALISIS VENTAS") \
    .config("spark.driver.extraClassPath", "/opt/spark-apps/drivers/postgresql-42.7.3.jar:/opt/spark/jars/*") \
    .config("spark.executor.extraClassPath", "/opt/spark-apps/drivers/postgresql-42.7.3.jar:/opt/spark/jars/*") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Leer las tablas desde PostgreSQL
df_tienda = spark.read.jdbc(url=jdbc_url, table="datos_tienda", properties=connection_properties)
df_compra = spark.read.jdbc(url=jdbc_url, table="datos_compra", properties=connection_properties)

# Renombrar las columnas para mayor claridad y consistencia
df_tienda = df_tienda.withColumnRenamed("store_id", "store_ID") \
                     .withColumnRenamed("store_name", "store_name") \
                     .withColumnRenamed("location", "location") \
                     .withColumnRenamed("demographics", "demographics")

df_compra = df_compra.withColumnRenamed("date", "date") \
                     .withColumnRenamed("store_ID", "store_ID") \
                     .withColumnRenamed("product_ID", "product_ID") \
                     .withColumnRenamed("quantity_Sold", "quantity_Sold") \
                     .withColumnRenamed("revenue", "revenue") \
                     .withColumnRenamed("Tratado", "Tratado") \
                     .withColumnRenamed("fecha_Insercion", "fecha_Insercion")

# Unir los datos de compras con los datos de tiendas por store_ID
df_joined = df_compra.join(df_tienda, "store_ID", "inner")

# a) ¿Qué tienda tiene los mayores ingresos totales?
df_grouped = df_joined.groupBy("store_name").agg(sum("revenue").alias("total_revenue"))
max_revenue = df_grouped.agg(max("total_revenue")).collect()[0][0]
df_stores_max = df_grouped.filter(col("total_revenue") == max_revenue)
df_top_stores = df_stores_max.join(df_tienda, "store_ID", "inner")

print('\n Tienda con más beneficios de venta: \n')
df_top_stores.show()

# b) ¿Cuáles son los ingresos totales generados en una fecha concreta?
fecha_concreta = '2025-03-25'  # Reemplaza con la fecha que necesites
df_quantity_date = df_joined.groupBy("date").agg(sum("revenue").alias("total_revenue"))
df_quantity_date_exact = df_quantity_date.filter(col("date") == to_timestamp(lit(fecha_concreta), 'yyyy-MM-dd'))

print('\n Ingresos en la fecha concreta: \n')
df_quantity_date_exact.show()

# c) ¿Qué producto tiene la mayor cantidad vendida?
df_products_group = df_joined.groupBy("product_ID").agg(sum("quantity_Sold").alias("total_sold"))
max_sold = df_products_group.agg(max("total_sold")).collect()[0][0]
df_products_max = df_products_group.filter(col("total_sold") == max_sold)
df_top_product = df_products_max.join(df_compra, "product_ID", "inner")

print('\n Producto más vendido: \n')
df_top_product.show()

# Detener Spark
spark.stop()
