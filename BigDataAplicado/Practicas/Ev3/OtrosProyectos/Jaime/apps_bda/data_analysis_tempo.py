from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, weekofyear, month, dayofweek, year

# Configuración de acceso a PostgreSQL
jdbc_url = "jdbc:postgresql://postgres-db:5432/retail_db"
connection_properties = {
    "user": "postgres",
    "password": "casa1234",
    "driver": "org.postgresql.Driver"
}

# Inicializa Spark
spark = SparkSession.builder \
    .appName("Análisis temporal de ventas") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3") \
    .getOrCreate()

# Leer la tabla 'tempo_ventas' desde PostgreSQL
tempo_ventas = spark.read.jdbc(url=jdbc_url, table="tempo_ventas", properties=connection_properties)

# Asegurarse de que 'revenue' y 'quantity_sold' sean numéricos (DoubleType)
tempo_ventas = tempo_ventas.withColumn("revenue", col("revenue").cast("double"))
tempo_ventas = tempo_ventas.withColumn("quantity_sold", col("quantity_sold").cast("double"))

# 1. ¿Cómo varía el rendimiento de las ventas a lo largo del tiempo? (diariamente, semanalmente, mensualmente)
# Para este análisis, vamos a agregar por fecha, semana y mes.

# Análisis Diario
ventas_diarias = tempo_ventas.groupBy("date") \
    .agg(
        sum("revenue").alias("total_revenue"),
        avg("revenue").alias("avg_revenue"),
        sum("quantity_sold").alias("total_quantity_sold")
    ) \
    .orderBy("date")

print("Rendimiento de las ventas a lo largo del tiempo (diariamente):")
ventas_diarias.show()

# Análisis Semanal
ventas_semanales = tempo_ventas.withColumn("week_of_year", weekofyear(col("date"))) \
    .groupBy("week_of_year") \
    .agg(
        sum("revenue").alias("total_revenue"),
        avg("revenue").alias("avg_revenue"),
        sum("quantity_sold").alias("total_quantity_sold")
    ) \
    .orderBy("week_of_year")

print("Rendimiento de las ventas a lo largo del tiempo (semanalmente):")
ventas_semanales.show()

# Análisis Mensual
ventas_mensuales = tempo_ventas.withColumn("month", month(col("date"))) \
    .groupBy("month") \
    .agg(
        sum("revenue").alias("total_revenue"),
        avg("revenue").alias("avg_revenue"),
        sum("quantity_sold").alias("total_quantity_sold")
    ) \
    .orderBy("month")

print("Rendimiento de las ventas a lo largo del tiempo (mensualmente):")
ventas_mensuales.show()

# 2. ¿Existen tendencias estacionales en las ventas?
# Para esto, podemos hacer un análisis mensual y observar los patrones estacionales en los ingresos y las cantidades vendidas.

# Tendencias estacionales por mes
tendencias_estacionales = ventas_mensuales.orderBy("month")

print("Tendencias estacionales en las ventas (por mes):")
tendencias_estacionales.show()

# Detener Spark
spark.stop()
