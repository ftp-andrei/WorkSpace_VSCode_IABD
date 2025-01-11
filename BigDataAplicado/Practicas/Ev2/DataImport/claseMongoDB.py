from pymongo import MongoClient
import json
import csv


def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Archivo no encontrado: {filename}")
        return None


def csv_a_json(csv_file, json_file):
    with open(csv_file, mode="r", encoding="utf-8") as file_csv:
        reader = csv.DictReader(file_csv)
        filas = [fila for fila in reader]

    with open(json_file, mode="w", encoding="utf-8") as file_json:
        json.dump(filas, file_json, indent=4, ensure_ascii=False)

    print(f"Archivo JSON generado correctamente: {json_file}")


class MongoDB:
    def __init__(self, database_name, port, username=None, password=None):
        if username and password:
            self.client = MongoClient(f'mongodb://{username}:{password}@localhost:{port}/')
        else:
            self.client = MongoClient(f'mongodb://localhost:{port}/')
        self.db = self.client[database_name]

    def insert_many(self, collection_name, data):
        collection = self.db[collection_name]
        if isinstance(data, list):
            result = collection.insert_many(data)
            print(f"{len(result.inserted_ids)} documentos insertados en la colección '{collection_name}'.")
        else:
            print("El formato de los datos no es una lista de documentos.")


# Convertir CSV a JSON
csv_a_json("Archivos/projects.csv", "Archivos/projects.json")
csv_a_json("Archivos/teams.csv", "Archivos/teams.json")
csv_a_json("Archivos/works_in_team.csv", "Archivos/works_in_team.json")

# Leer los archivos JSON
favourite_pokemon = read_json_file("Archivos/favourite_pokemon.json")
projects = read_json_file("Archivos/projects.json")
teams = read_json_file("Archivos/teams.json")
works_in_team = read_json_file("Archivos/works_in_team.json")

# Conectar a MongoDB
mongo_operations = MongoDB('Acomodations', '27017')

# Insertamos los datos
mongo_operations.insert_many("works_in_team", works_in_team)
mongo_operations.insert_many("projects", projects)
mongo_operations.insert_many("teams", teams)
mongo_operations.insert_many("works_in_team", works_in_team)
