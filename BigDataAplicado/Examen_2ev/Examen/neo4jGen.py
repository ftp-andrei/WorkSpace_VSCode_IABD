
import random
from neo4j import GraphDatabase
from faker import Faker
uri = "bolt://localhost:7687"
user = "neo4j"
password = "my-secret-pw" # original: password

fake = Faker("es_ES")

driver = GraphDatabase.driver(uri, auth=(user, password))

def insert_data(tx):
    for i in range(1, 30):
        tx.run("CREATE (:Parada {id: $id, nombre: $nombre})",
               id=i, nombre=f"Parada {fake.name()}")
    
    for i in range(1, 100):
        tx.run("CREATE (:Vehiculo {id: $id, linea: $linea})",
               id=f"Bus_{i}" if random.random() < 0.7 else f"Tranvia_{i}", linea=f"L{random.randint(1, 100)}")

    for _ in range(200):
        vehiculo_id = f"Bus_{random.randint(1, 100)}" if random.random() < 0.7 else f"Tranvia_{random.randint(1, 100)}"
        parada_id = random.randint(1, 40)
        tx.run("""
            MATCH (v:Vehiculo {id: $vehiculo_id}), (p:Parada {id: $parada_id})
            CREATE (v)-[:PARA_EN]->(p)
        """, vehiculo_id=vehiculo_id, parada_id=parada_id)

with driver.session() as session:
    session.execute_write(insert_data)

print("Datos insertados en Neo4j.")

driver.close()
