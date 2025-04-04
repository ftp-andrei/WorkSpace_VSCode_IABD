from time import sleep
from json import dumps
from kafka import KafkaProducer
from datetime import datetime
from faker import Faker
import random

fake = Faker()

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))
print("Escuchando ...")
while True:
    message = {
        "timestamp": int(datetime.now().timestamp() * 1000),
        "evento": fake.address(),
        "nombre": fake.name(),  
        "equipo": fake.city_name(),  
        "resultado": round(random.uniform(100.0, 1000.0), 2)  
    }
    producer.send('sales_stream', value=message)
    sleep(1)
