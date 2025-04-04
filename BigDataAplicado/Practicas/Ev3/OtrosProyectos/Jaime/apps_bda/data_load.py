from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Configuración de acceso a S3 (Localstack)
aws_access_key_id = 'test'
aws_secret_access_key = 'test'

# Inicializa Spark
spark = SparkSession.builder \
    .appName("Carga DW desde S3") \
    .config("spark.streaming.stopGracefullyOnShutdown", True) \
    .config("spark.sql.shuffle.partitions", 4) \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
    .config("spark.jars.packages", 
        "org.apache.spark:spark-hadoop-cloud_2.13:3.5.1,"
        "software.amazon.awssdk:s3:2.25.11,"
        "org.postgresql:postgresql:42.7.3") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.driver.extraClassPath", "/opt/spark-apps/postgresql-42.7.3.jar") \
    .config("spark.executor.extraClassPath", "/opt/spark-apps/postgresql-42.7.3.jar") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Función para cargar datos en PostgreSQL usando PySpark
def load_to_postgresql(df, table_name):
    jdbc_url = "jdbc:postgresql://postgres-db:5432/retail_db"
    connection_properties = {
        "user": "postgres",
        "password": "casa1234",
        "driver": "org.postgresql.Driver"
    }

    df.write.jdbc(url=jdbc_url, table=table_name, mode='overwrite', properties=connection_properties)
    print(f"Datos cargados correctamente en la tabla {table_name}.")

try:
    # Leer datos_tienda (1 archivo)
    df_tienda = spark.read.option("header", True).csv("s3a://cubito/processed/datos_tienda")

    # Leer datos_compra (varios archivos)
    df_compra = spark.read.option("header", True).csv("s3a://cubito/processed/datos_compra")

    # Mostrar los dataframes para validar
    print("Datos de tienda:")
    df_tienda.show()
    print("Datos de compra:")
    df_compra.show()

    # Renombrar columnas para permitir join
    df_tienda = df_tienda.withColumnRenamed("_c0", "store_id") \
                        .withColumnRenamed("_c1", "store_name") \
                        .withColumnRenamed("_c2", "location") \
                        .withColumnRenamed("_c3", "demographics")

    # Renombrar columnas para facilitar el join
    df_compra = df_compra.withColumnRenamed("_c1", "store_id") \
                        .withColumnRenamed("_c2", "product_id") \
                        .withColumnRenamed("_c3", "quantity_sold") \
                        .withColumnRenamed("_c4", "revenue") \
                        .withColumnRenamed("_c0", "date")

    # Hacer el join ahora que ambas tienen 'store_id'
    df_joined = df_compra.join(df_tienda, on="store_id", how="inner")

    # Crear tabla Ventas
    ventas = df_joined.select(
        "store_id", "store_name", "product_id", "quantity_sold", "revenue", "date"
    )
    load_to_postgresql(ventas, "ventas")

    # Crear tabla Geo_Ventas
    geo_ventas = df_joined.select(
        "location", "store_id", "product_id", "quantity_sold", "revenue"
    )
    load_to_postgresql(geo_ventas, "geo_ventas")

    # Crear tabla Demo_Ventas
    demo_ventas = df_joined.select(
        "demographics", "store_id", "product_id", "quantity_sold", "revenue"
    )
    load_to_postgresql(demo_ventas, "demo_ventas")

    # Crear tabla Tempo_Ventas
    tempo_ventas = df_joined.select(
        "date", "store_id", "product_id", "quantity_sold", "revenue"
    )
    load_to_postgresql(tempo_ventas, "tempo_ventas")

    print("Todas las tablas se han cargado exitosamente en el Data Warehouse.")

except Exception as e:
    print("Error en el pipeline:", e)

finally:
    spark.stop()
