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
    .appName("Analisis") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3") \
    .getOrCreate()

geo_ventas = spark.read.jdbc(url=jdbc_url, table="geo_ventas", properties=connection_properties)

geo_ventas = geo_ventas.withColumn("Estadísticas", col("HP"))
geo_ventas = geo_ventas.withColumn("Estadísticas", col("Ataque"))

# 1. Cuáles son los Pokémon con mayor HP
regiones_mejores_ingresos = geo_ventas.groupBy("Estadísticas") \
    .sum("HP") \
    .withColumnRenamed("sum(HP)", "total_HP") \
    .orderBy("total_HP", ascending=False)

# 2. Qué Pokémon tiene el mayor ataque
regiones_mejores_ingresos = geo_ventas.groupBy("Estadísticas") \
    .sum("Ataque") \
    .withColumnRenamed("sum(Ataque)", "total_Ataque") \
    .orderBy("total_Ataque", ascending=False)