from pymongo import MongoClient
import json

def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return None
    
class MongoDBOperations:
    def __init__(self, database_name, port,username=None, password=None):
        if username and password:
            self.client = MongoClient(f'mongodb://{username}:{password}@localhost:{{port}}/')
        else:
            self.client = MongoClient(f'mongodb://localhost:{port}/')
        self.db = self.client[database_name]
        
    def create_person(self, collection_name,data):
        self.collection = self.db[collection_name]
        result = self.collection.insert_one(data)
        return result
    
favourite_pokemon=read_json_file("Archivos/favourite_pokemon.json")

# Pasar de csv a JSON

works_in_team=read_json_file("Archivos/works_in_team.csv")
teams=read_json_file("Archivos/teams.csv")
projects=read_json_file("Archivos/projects.csv")


mongo_operations = MongoDBOperations('Acomodations','32769')

for data in favourite_pokemon:
    mongo_operations.create_person("destinations",data)


