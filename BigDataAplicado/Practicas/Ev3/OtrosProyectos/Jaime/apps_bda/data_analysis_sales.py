from pyspark.sql import SparkSession

# Configuración de acceso a PostgreSQL
jdbc_url = "jdbc:postgresql://postgres-db:5432/retail_db"
connection_properties = {
    "user": "postgres",
    "password": "casa1234",
    "driver": "org.postgresql.Driver"
}

# Inicializa Spark
spark = SparkSession.builder \
    .appName("Consulta de ventas") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3") \
    .getOrCreate()

ventas = spark.read.jdbc(url=jdbc_url, table="ventas", properties=connection_properties)

from pyspark.sql.functions import col, avg, when, to_date

ventas = ventas.withColumn("revenue", col("revenue").cast("double"))
ventas = ventas.withColumn("quantity_sold", col("quantity_sold").cast("double"))

# 1. Tienda con los mayores ingresos totales
tienda_mayores_ingresos = ventas.groupBy("store_name") \
    .sum("revenue") \
    .withColumnRenamed("sum(revenue)", "total_revenue") \
    .orderBy("total_revenue", ascending=False) \
    .limit(1)

print("Tienda con los mayores ingresos totales:")
tienda_mayores_ingresos.show()

# 2. Ingresos totales generados en una fecha concreta

fecha_concreta = '2009-10-04'

ingresos_fecha = ventas.filter(ventas["date"] == fecha_concreta) \
    .groupBy("date") \
    .sum("revenue") \
    .withColumnRenamed("sum(revenue)", "total_revenue")

print(f"Ingresos totales generados el {fecha_concreta}:")
ingresos_fecha.show()

# 3. Producto con la mayor cantidad vendida
producto_mayor_cantidad = ventas.groupBy("product_id") \
    .sum("quantity_sold") \
    .withColumnRenamed("sum(quantity_sold)", "total_quantity_sold") \
    .orderBy("total_quantity_sold", ascending=False) \
    .limit(1)

print("Producto con la mayor cantidad vendida:")
producto_mayor_cantidad.show()

# Detener Spark
spark.stop()
