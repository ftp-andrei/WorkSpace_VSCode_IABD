#Características de Pokémon:
#¿Cuáles son los Pokémon con mayor HP?
#¿Qué Pokémon tiene el mayor ataque?
#¿Cuáles son las habilidades más comunes entre los Pokémon?
'''
PokemonName
PokemonHP
PokemonAtack
PokemonHabilities
'''

#Comportamiento del entrenador:
#¿Quién es el entrenador con más victorias registradas?
#¿Cuál es el equipo de Pokémon más utilizado por los entrenadores ganadores?
#¿Existe alguna correlación entre el tipo de Pokémon y el resultado de la batalla?
'''
TrainerName
Victorias
MostUsedTeam
MostUsedType
'''

#Eventos especiales de Pokémon:
#¿Cuántos eventos especiales se han registrado en la base de datos?
#¿Cuál fue el evento más reciente?
#¿Qué descripción tiene el evento con más batallas?
'''
eventoName
eventoFecha
Descripcion
NumBatallas
'''

from pyspark.sql import SparkSession
aws_access_key_id = 'test'
aws_secret_access_key = 'test'

class Evento:
    Descripcion: str
    Evento: str
    Fecha: str
    
try:
    spark = SparkSession.builder \
    .appName("SPARK S3") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localstack:4566") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
    .config("spark.sql.shuffle.partitions", "4") \
    .config("spark.jars.packages","org.apache.spark:spark-hadoop-cloud_2.13:3.5.1,software.amazon.awssdk:s3:2.25.11") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.driver.extraClassPath", "/opt/spark/jars/s3-2.25.11.jar") \
    .config("spark.executor.extraClassPath", "/opt/spark/jars/s3-2.25.11.jar") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

    
    dfBattleRecord = spark.read.text("s3a://bucket/pokemon_battle_events-json")
    
    lines = dfBattleRecord.rdd.map(lambda r: list(r)).collect()
    contador=0
    for line in lines:
        
        contadot=contador+1
        print(line)
    
    
    dfPokemon = spark.read.json("s3a://bucket/pokemon_data-json")

    
    dfEvent = spark.read.json("s3a://bucket/pokemon_battle_events-json")
    data=dfEvent.take(5)
    print(data[0].Descripcion)
    print(data[0])
    print(data)
    
    spark.stop()
    
except Exception as e:
    print(e)
    