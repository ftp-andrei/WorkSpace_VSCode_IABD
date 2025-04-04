from pyspark.sql import SparkSession
# Cuando trabajas con Neo4j, puedes seleccionar columnas específicas utilizando 
# la opción query en el conector de Neo4j
# Configuración de Spark
spark = SparkSession.builder \
    .appName("Neo4j to S3") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
    .config("spark.hadoop.fs.s3a.access.key", "test") \
    .config("spark.hadoop.fs.s3a.secret.key", "test") \
    .config("spark.jars.packages", "neo4j-contrib:neo4j-spark-connector:4.0.0") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Conexión a Neo4j
neo4j_url = "bolt://neo4j:7687"
neo4j_user = "neo4j"
neo4j_password = "password"

# Seleccionar columnas específicas de un nodo en Neo4j
query = "MATCH (p:Product) RETURN p.id AS id, p.name AS name, p.price AS price"
df_neo4j = spark.read.format("org.neo4j.spark.DataSource") \
    .option("url", neo4j_url) \
    .option("authentication.type", "basic") \
    .option("authentication.basic.username", neo4j_user) \
    .option("authentication.basic.password", neo4j_password) \
    .option("query", query) \
    .load()

# Mostrar el DataFrame resultante
df_neo4j.show()

# Guardar en S3
df_neo4j.write.mode('overwrite').csv('s3a://bucket/neo4j_data', header=True, sep=',')

spark.stop()
