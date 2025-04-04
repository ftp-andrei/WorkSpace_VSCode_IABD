import json
import random
from faker import Faker

fake = Faker()

TYPES = ["Planta", "Fuego", "Agua", "Eléctrico", "Hielo", "Lucha", "Veneno", "Tierra", "Volador", "Psíquico", "Bicho", "Roca", "Fantasma", "Dragón", "Siniestro", "Acero", "Hada"]
ABILITIES = ["Intimidación", "Cuerpo llama", "Absorbe agua", "Espesura", "Clorofila", "Levitación", "Rayo solar"]

# Generar pokemon_data.json
pokemon_data = []
for _ in range(3000):
    name = fake.first_name()
    type_ = random.choice(TYPES)
    stats = {"HP": random.randint(20, 200), "Ataque": random.randint(10, 150), "Defensa": random.randint(10, 150), "Velocidad": random.randint(10, 150)}
    abilities = random.sample(ABILITIES, k=random.randint(1, 3))
    evolutions = [{"Nombre": fake.first_name(), "Tipo": random.choice(TYPES)} for _ in range(random.randint(0, 2))]
    
    pokemon_data.append({"Nombre": name, "Tipo": type_, "Estadísticas": stats, "Habilidades": abilities, "Evoluciones": evolutions})

with open("pokemon_data.json", "w", encoding="utf-8") as f:
    json.dump(pokemon_data, f, indent=2, ensure_ascii=False)

# Generar battle_records.txt
battle_records = []
for _ in range(10000):
    event = fake.city() + " Tournament"
    trainer = fake.name()
    team = random.sample([p["Nombre"] for p in pokemon_data], k=random.randint(3, 6))
    result = random.choice(["Ganó", "Perdió"])
    
    battle_records.append(f"Evento: {event}\nNombre del entrenador: {trainer}\nEquipo de Pokémon: {team}\nResultado de la batalla: {result}\n")

with open("battle_records.txt", "w", encoding="utf-8") as f:
    f.writelines(battle_records)

# Generar pokemon_battle_events.json
pokemon_battle_events = []
for _ in range(10000):
    timestamp = fake.iso8601()
    event = fake.city() + " Cup"
    trainer = fake.name()
    team = random.sample([p["Nombre"] for p in pokemon_data], k=random.randint(3, 6))
    result = random.choice(["Ganó", "Perdió"])
    
    pokemon_battle_events.append({"Timestamp": timestamp, "Evento": event, "Nombre del entrenador": trainer, "Equipo de Pokémon": team, "Resultado de la batalla": result})

with open("pokemon_battle_events.json", "w", encoding="utf-8") as f:
    json.dump(pokemon_battle_events, f, indent=2, ensure_ascii=False)

# Generar pokemon_events.json para MongoDB
pokemon_events = []
for _ in range(1000):
    event = fake.city() + " Pokémon Festival"
    date = fake.date()
    description = fake.sentence()
    
    pokemon_events.append({"Evento": event, "Fecha": date, "Descripción": description})

with open("pokemon_events.json", "w", encoding="utf-8") as f:
    json.dump(pokemon_events, f, indent=2, ensure_ascii=False)

print("Archivos generados correctamente.")
