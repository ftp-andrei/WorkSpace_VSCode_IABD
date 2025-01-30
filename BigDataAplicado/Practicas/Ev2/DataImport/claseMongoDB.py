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
            self.client = MongoClient(f'mongodb://{username}:{password}@localhost:7777/')
        else:
            self.client = MongoClient(f'mongodb://localhost:{port}/')
        self.db = self.client[database_name]

    def insert_many(self, collection_name, data):
        collection = self.db[collection_name]
        # Verificar si la colección ya existe y contiene datos
        if collection.estimated_document_count() > 0:
            print(f"La colección '{collection_name}' ya contiene datos. No se insertarán nuevos documentos.")
            return
        # Insertar documentos si la colección está vacía
        if isinstance(data, list):
            result = collection.insert_many(data)
            print(f"{len(result.inserted_ids)} documentos insertados en la colección '{collection_name}'.")
        else:
            print("El formato de los datos no es una lista de documentos.")

    def close(self):
        self.client.close()

#------------------CONSULTAS-------------------------  
        
    # Función para obtener personas y roles de un equipo específico (ID_PERSON, ROL)
    def consulta4(self, team_name):
        pipeline = [
            {
                "$lookup": {
                    "from": "teams",           # Colección con la que unimos
                    "localField": "team_id",   # Campo en works_in_team
                    "foreignField": "team_id", # Campo en teams
                    "as": "team_info"          # Alias para los datos unidos
                }
            },
            {
                "$unwind": "$team_info"         # Desanidar el array de team_info
            },
            {
                "$match": { 
                    "team_info.name": team_name # Filtrar por el nombre del equipo
                }
            },
            {
                "$group": {                     # Agrupar para evitar duplicados
                    "_id": {                    # Agrupamos por persona y rol
                        "person_id": "$person_id",
                        "rol": "$rol"
                    },
                    "team_info": { "$first": "$team_info" }  # Retener el primer valor de team_info
                }
            },
            {
                "$project": {                   # Seleccionar los campos deseados
                    "_id": 0,
                    "person_id": "$_id.person_id",
                    "rol": "$_id.rol",
                }
            }
        ]
        
        # Ejecutar el pipeline
        results = list(self.db["works_in_team"].aggregate(pipeline))
        return results

    # Función para obtener el nombre de los equipos y el conteo de personas
    def consulta5(self):
        pipeline = [
            {
                "$lookup": {
                    "from": "teams",           # Colección con la que unimos
                    "localField": "team_id",   # Campo en works_in_team
                    "foreignField": "team_id", # Campo en teams
                    "as": "team_info"          # Alias para los datos unidos
                }
            },
            {
                "$unwind": {
                    "path": "$team_info",       # Desanidar el array de team_info
                    "preserveNullAndEmptyArrays": False  # Ignorar documentos sin coincidencia
                }
            },
            {
                "$group": {
                    "_id": "$team_info.name",  # Agrupar por nombre del equipo
                    "num_people": { "$sum": 1 }  # Contar el número de personas en el equipo
                }
            },
            {
                "$project": {
                    "_id": 0,                  # Ocultar el _id
                    "team_name": "$_id",       # Nombre del equipo
                    "num_people": 1            # Conteo de personas
                }
            },
            {
                "$sort": {
                    "team_name": 1             # Ordenar por nombre del equipo
                }
            }
        ]
        
        # Ejecutar el pipeline
        results = list(self.db["works_in_team"].aggregate(pipeline))
        
        # Mostrar los resultados en consola
        for result in results:
            print(f"Equipo: {result['team_name']}, Número de personas: {result['num_people']}")


    # Muestra los equipos con el número total de proyectos a los que están asociados
    def consulta6(self):
        pipeline = [
            # Unir con la colección "projects" para obtener el nombre del proyecto
            {
                "$lookup": {
                    "from": "projects",          # Colección a unir
                    "localField": "project_id",  # Campo en "teams"
                    "foreignField": "project_id",# Campo en "projects"
                    "as": "project_info"         # Alias para los datos del proyecto
                }
            },
            # Desanidar el array project_info (1 documento por proyecto)
            {"$unwind": "$project_info"},
            # Agrupar por nombre del proyecto y contar equipos
            {
                "$group": {
                    "_id": "$project_info.name",  # Agrupar por nombre del proyecto
                    "total_equipos": {"$sum": 1}  # Contar equipos en cada proyecto
                }
            },
            # Proyectar campos deseados
            {
                "$project": {
                    "_id": 0, 
                    "nombre_proyecto": "$_id", 
                    "equipos_asociados": "$total_equipos"
                }
            },
            # Ordenar por nombre del proyecto
            {"$sort": {"nombre_proyecto": 1}}
        ]
        
        results = list(self.db["teams"].aggregate(pipeline))
        
        # Mostrar resultados
        for result in results:
            print(f"Proyecto: {result['nombre_proyecto']}, Nº asociados: {result['equipos_asociados']}")

    #Dado una ubicación, obtén la lista de equipos que están ubicados allí junto
    #con información de las personas que trabajan en ese equipo y los proyectos asociados.
    def consulta10(self, location_id):
        pipeline = [
            {
                "$lookup": {
                    "from": "teams",
                    "localField": "team_id",
                    "foreignField": "team_id",
                    "as": "team_info"
                }
            },
            {
                "$unwind": {
                    "path": "$team_info",
                }
            },
            {
                "$lookup": {
                    "from": "projects",
                    "localField": "team_info.project_id",
                    "foreignField": "project_id",
                    "as": "project_info"
                }
            },
            {
                "$unwind": {
                    "path": "$project_info",
                }
            },
            {
                "$match": {
                    "project_info.location_id": location_id
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "person_id": 1,
                    "team_name": "$team_info.name",
                    "project_name": "$project_info.name"
                }
            }
        ]
        
        result = list(self.db["works_in_team"].aggregate(pipeline))        
        return result



# Convertir CSV a JSON
csv_a_json("Archivos/MongoDB/projects.csv", "Archivos/MongoDB/projects.json")
csv_a_json("Archivos/MongoDB/teams.csv", "Archivos/MongoDB/teams.json")
csv_a_json("Archivos/MongoDB/works_in_team.csv", "Archivos/MongoDB/works_in_team.json")

# Leer los archivos JSON
favourite_pokemon = read_json_file("Archivos/MongoDB/favourite_pokemon.json")
projects = read_json_file("Archivos/MongoDB/projects.json")
teams = read_json_file("Archivos/MongoDB/teams.json")
works_in_team = read_json_file("Archivos/MongoDB/works_in_team.json")

# Conectar a MongoDB usando credenciales
mongo_operations = MongoDB(database_name='PokemonDB', port='27017', username='mongoadmin', password='secret')

# Insertamos los datos
mongo_operations.insert_many("favourite_pokemon", favourite_pokemon)
mongo_operations.insert_many("projects", projects)
mongo_operations.insert_many("teams", teams)
mongo_operations.insert_many("works_in_team", works_in_team)

print("Mongo: Datos insertados correctamente.") 

