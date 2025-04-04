from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, when

# Configuración de acceso a PostgreSQL
jdbc_url = "jdbc:postgresql://postgres-db:5432/retail_db"
connection_properties = {
    "user": "postgres",
    "password": "casa1234",
    "driver": "org.postgresql.Driver"
}

# Inicializa Spark
spark = SparkSession.builder \
    .appName("Análisis demográfico de ventas") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3") \
    .getOrCreate()

# Leer la tabla 'demo_ventas' desde PostgreSQL
demo_ventas = spark.read.jdbc(url=jdbc_url, table="demo_ventas", properties=connection_properties)

demo_ventas = demo_ventas.withColumn("revenue", col("revenue").cast("double"))
demo_ventas = demo_ventas.withColumn("quantity_sold", col("quantity_sold").cast("double"))

# 1. ¿Cómo varía el rendimiento de las ventas entre los distintos grupos demográficos?
ventas_por_demografico = demo_ventas.groupBy("demographics") \
    .agg(
        sum("revenue").alias("total_revenue"),
        avg("revenue").alias("avg_revenue"),
        sum("quantity_sold").alias("total")
    ) \
    .orderBy("total_revenue", ascending=False)

print("Rendimiento de las ventas entre los distintos grupos demográficos:")
ventas_por_demografico.show()

# 2. ¿Existen productos específicos preferidos por determinados grupos demográficos?
productos_por_demografico = demo_ventas.groupBy("demographics", "product_id") \
    .agg(
        sum("quantity_sold").alias("total")
    ) \
    .orderBy("total", ascending=False)

print("Productos preferidos por distintos grupos demográficos:")
productos_por_demografico.show()

# Detener Spark
spark.stop()
