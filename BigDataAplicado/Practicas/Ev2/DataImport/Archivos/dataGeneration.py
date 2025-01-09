import csv
import json
import random
from datetime import datetime

# Generate CSV files for Neo4j data
def generate_neo4j_data():
    # persons.csv
    with open('BigDataAplicado/Practicas/Ev2/DataImport/Archivos/dataGeneration.py/persons.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'age'])
        for i in range(1, 101):
            writer.writerow([i, f'Person_{i}', random.randint(18, 65)])

    # empresas.csv
    with open('BigDataAplicado/Practicas/Ev2/DataImport/Archivos/dataGeneration.py/empresas.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'sector'])
        sectors = ['Tech', 'Finance', 'Healthcare', 'Education']
        for i in range(1, 51):
            writer.writerow([i, f'Company_{i}', random.choice(sectors)])

    # works_at.csv
    with open('BigDataAplicado/Practicas/Ev2/DataImport/Archivos/dataGeneration.py/works_at.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['rol', 'location_id'])
        roles = ['Engineer', 'Manager', 'Analyst', 'Developer']
        for i in range(1, 101):
            writer.writerow([random.choice(roles), random.randint(1, 20)])

# Generate JSON files for MySQL data
def generate_mysql_data():
    # locations.json
    locations = [{'id': i, 'name': f'Location_{i}', 'city': f'City_{i}'} for i in range(1, 21)]
    with open('BigDataAplicado/Practicas/Ev2/DataImport/Archivos/dataGeneration.py/locations.json', 'w') as file:
        json.dump(locations, file, indent=4)

    # skills.json
    skills = [{'id': i, 'name': f'Skill_{i}'} for i in range(1, 51)]
    with open('BigDataAplicado/Practicas/Ev2/DataImport/Archivos/dataGeneration.py/skills.json', 'w') as file:
        json.dump(skills, file, indent=4)

    # has_skill.json
    has_skill = [{'person_id': random.randint(1, 100), 'skill_id': random.randint(1, 50), 'proficiency': random.choice(['Beginner', 'Intermediate', 'Expert'])} for _ in range(200)]
    with open('BigDataAplicado/Practicas/Ev2/DataImport/Archivos/dataGeneration.py/has_skill.json', 'w') as file:
        json.dump(has_skill, file, indent=4)

    # pokemon.json
    pokemon = [{'pokemon_id': i, 'description': f'Description_{i}', 'pokeGame': f'Game_{i}'} for i in range(1, 151)]
    with open('BigDataAplicado/Practicas/Ev2/DataImport/Archivos/dataGeneration.py/pokemon.json', 'w') as file:
        json.dump(pokemon, file, indent=4)

# Generate CSV and JSON files for MongoDB data
def generate_mongodb_data():
    # projects.csv
    with open('BigDataAplicado/Practicas/Ev2/DataImport/Archivos/dataGeneration.py/projects.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['project_id', 'name', 'description', 'location_id', 'company_id'])
        for i in range(1, 31):
            writer.writerow([i, f'Project_{i}', f'Description_{i}', random.randint(1, 20), random.randint(1, 50)])

    # teams.csv
    with open('BigDataAplicado/Practicas/Ev2/DataImport/Archivos/dataGeneration.py/teams.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['team_id', 'name', 'description', 'project_id'])
        for i in range(1, 31):
            writer.writerow([i, f'Team_{i}', f'Description_{i}', random.randint(1, 30)])

    # works_in_team.csv
    with open('BigDataAplicado/Practicas/Ev2/DataImport/Archivos/dataGeneration.py/works_in_team.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['person_id', 'team_id', 'rol'])
        roles = ['Leader', 'Member', 'Support']
        for _ in range(200):
            writer.writerow([random.randint(1, 100), random.randint(1, 30), random.choice(roles)])

    # favourite_pokemon.json
    favourite_pokemon = [{'person_id': random.randint(1, 100), 'pokemon_id': random.randint(1, 150), 'dateCaptured': datetime.now().strftime('%Y-%m-%d')} for _ in range(100)]
    with open('BigDataAplicado/Practicas/Ev2/DataImport/Archivos/dataGeneration.py/favourite_pokemon.json', 'w') as file:
        json.dump(favourite_pokemon, file, indent=4)

if __name__ == "__main__":
    generate_neo4j_data()
    generate_mysql_data()
    generate_mongodb_data()
    print("Data files generated successfully.")
