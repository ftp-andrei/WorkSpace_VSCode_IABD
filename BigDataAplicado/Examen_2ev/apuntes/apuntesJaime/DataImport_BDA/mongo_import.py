import json

from Database.mainMongo import MongoDBOperations

def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return None
    

"""
def read_csv_file(filename):
    data = []
    with open(filename, 'r', encoding='utf-8' ) as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(dict(row))
    return data
"""   
favourite_pokemon=read_json_file("mongo/favourite_pokemon.json")
projects=read_json_file("mongo/projects.json")
teams=read_json_file("mongo/teams.json")
works_in_team=read_json_file("mongo/works_in_team.json")


MONGO_DATABASE = "Trafabajo2"
MONGO_PORT = "7777"
MONGO_USER = "mongoadmin"
MONGO_PASSWORD = "secret"

mongo_operations = MongoDBOperations(MONGO_DATABASE, MONGO_PORT, MONGO_USER, MONGO_PASSWORD)

for data in favourite_pokemon:
    mongo_operations.create_person("favourite_pokemon",data)

for data in projects:
    mongo_operations.create_person("projects",data)

for data in teams:
    mongo_operations.create_person("teams",data)

for data in works_in_team:
    mongo_operations.create_person("works_in_team",data)
    