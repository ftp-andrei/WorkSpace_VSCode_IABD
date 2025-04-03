from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, current_timestamp, mean, count
from pyspark.sql.types import IntegerType, FloatType, TimestampType
import re
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, TimestampType, StringType


# Inicializar la sesión de Spark con configuración para LocalStack
spark = SparkSession.builder \
    .appName("DataTransformation") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
    .config("spark.hadoop.fs.s3a.access.key", "test") \
    .config("spark.hadoop.fs.s3a.secret.key", "test") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Cargar datos desde el Data Lake en LocalStack
# * = part de la ruta csv
data_path = "s3a://bucket/output/*.csv"

# Definir el esquema
schema = StructType([
    StructField("Date", TimestampType(), True),  # Campo de fecha
    StructField("Store ID", IntegerType(), True),  # ID de tienda
    StructField("Product ID", IntegerType(), True),  # ID de producto
    StructField("Quantity Sold", IntegerType(), True),  # Cantidad vendida
    StructField("Revenue", FloatType(), True)  # Ingresos
])
df = spark.read.option("header", "true").schema(schema).csv(data_path)

# Verificar los nombres originales de las columnas
print("Columnas originales:", df.columns)

# Limpiar nombres de columnas (eliminar caracteres especiales y espacios)
def clean_column_name(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)  # Reemplazar caracteres inválidos con '_'

df = df.toDF(*[clean_column_name(col_name) for col_name in df.columns])

# Tratamiento de valores perdidos
for column in df.columns:
    missing_count = df.filter(col(column).isNull()).count()
    if missing_count > 0:
        if df.select(column).schema.fields[0].dataType in [IntegerType(), FloatType()]:
            mean_value = df.select(mean(col(column))).collect()[0][0]
            df = df.fillna({column: mean_value})  # Imputación con la media
        else:
            df = df.na.drop(subset=[column])  # Eliminación de filas con valores nulos

# Agregar columnas adicionales
df = df.withColumn("Tratados", lit("Sí"))
df = df.withColumn("Fecha Inserción", current_timestamp())

# Guardar datos transformados en LocalStack en formato Parquet
output_path = "s3a://bucket/output/processed_data.parquet"
df.write.mode("overwrite").parquet(output_path)

# Mostrar el esquema del DataFrame transformado
df.printSchema()
df.show(10)  # Muestra las primeras 50 filas

print("Transformación completada y datos guardados correctamente.")