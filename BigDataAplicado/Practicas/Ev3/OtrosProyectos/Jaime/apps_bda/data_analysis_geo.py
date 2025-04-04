from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, corr

# Configuración de acceso a PostgreSQL
jdbc_url = "jdbc:postgresql://postgres-db:5432/retail_db"
connection_properties = {
    "user": "postgres",
    "password": "casa1234",
    "driver": "org.postgresql.Driver"
}

# Inicializa Spark
spark = SparkSession.builder \
    .appName("Análisis geográfico de ventas") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3") \
    .getOrCreate()

geo_ventas = spark.read.jdbc(url=jdbc_url, table="geo_ventas", properties=connection_properties)

geo_ventas = geo_ventas.withColumn("revenue", col("revenue").cast("double"))
geo_ventas = geo_ventas.withColumn("quantity_sold", col("quantity_sold").cast("double"))

# 1. Regiones con mejores resultados en función de los ingresos
regiones_mejores_ingresos = geo_ventas.groupBy("location") \
    .sum("revenue") \
    .withColumnRenamed("sum(revenue)", "total_revenue") \
    .orderBy("total_revenue", ascending=False)

print("Regiones con mejores resultados en función de los ingresos:")
regiones_mejores_ingresos.show()

# 2. Correlación entre la ubicación de la tienda y el rendimiento de las ventas

from pyspark.ml.feature import StringIndexer
indexer = StringIndexer(inputCol="location", outputCol="location_index")
geo_ventas = indexer.fit(geo_ventas).transform(geo_ventas)

# Calcular la correlación entre la ubicación y los ingresos
correlacion_ubicacion_ingresos = geo_ventas.select("location_index", "revenue").stat.corr("location_index", "revenue")

print(f"Correlación entre la ubicación de la tienda y el rendimiento de las ventas: {correlacion_ubicacion_ingresos}")

# Detener Spark
spark.stop()
