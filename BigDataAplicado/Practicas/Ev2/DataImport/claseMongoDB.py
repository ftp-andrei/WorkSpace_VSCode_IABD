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


def txt_a_csv(txt_file, csv_file):
    with open(txt_file, mode="r", encoding="utf-8") as file_txt:
        # Lee el archivo de texto línea por línea
        lines = file_txt.readlines()

    # Abre el archivo CSV para escribir
    with open(csv_file, mode="w", newline='', encoding="utf-8") as file_csv:
        writer = csv.writer(file_csv)

        # Si el archivo txt tiene cabeceras, puedes escribirlas en el CSV
        # Si no, salta este paso
        # writer.writerow(["columna1", "columna2", "columna3"])  # Modificar según tus necesidades

        # Procesar cada línea
        for line in lines:
            # Aquí definimos cómo separar los datos (por ejemplo, usando espacios o tabulaciones)
            # Si son separados por tabulaciones, puedes usar `split('\t')`
            row = line.split()  # Por defecto separa por espacios
            writer.writerow(row)

    print(f"Archivo CSV generado correctamente: {csv_file}")

def json_a_csv(json_file, csv_file):
    # Leer el archivo JSON
    with open(json_file, mode="r", encoding="utf-8") as file_json:
        data = json.load(file_json)

    # Abrir el archivo CSV para escribir
    with open(csv_file, mode="w", newline='', encoding="utf-8") as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=data[0].keys())

        # Escribir los encabezados (keys del primer diccionario)
        writer.writeheader()

        # Escribir los registros
        for record in data:
            writer.writerow(record)

    print(f"Archivo CSV generado correctamente: {csv_file}")


def txt_a_json(txt_file, json_file):
    with open(txt_file, mode="r", encoding="utf-8") as file_txt:
        lines = file_txt.readlines()

    # Asumiendo que cada línea contiene un registro y los campos están separados por espacios o tabulaciones
    data = []
    for line in lines:
        # Dividir la línea por espacios (puedes cambiar esto si es otro delimitador)
        fields = line.strip().split()
        # Crear un diccionario con claves generadas dinámicamente
        record = {
            "campo1": fields[0],
            "campo2": fields[1],
            "campo3": fields[2]  # Ajusta según el número de campos y tus necesidades
        }
        data.append(record)

    # Guardar los datos en un archivo JSON
    with open(json_file, mode="w", encoding="utf-8") as file_json:
        json.dump(data, file_json, indent=4, ensure_ascii=False)

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


    # Devuelve el proyecto que mas personas tiene
    def consulta9(self):
        pipeline = [
            # 1. Eliminar duplicados de personas en equipos
            {"$group": {
                "_id": {"person": "$person_id", "team": "$team_id"}
            }},
            
            # 2. Contar personas únicas por equipo (convertir team_id a string)
            {"$group": {
                "_id": {"$toString": "$_id.team"},  # Convertir a string para hacer match con teams
                "totalPersonas": {"$sum": 1}
            }},
            
            # 3. Unir con equipos (team_id como string)
            {"$lookup": {
                "from": "teams",
                "localField": "_id",
                "foreignField": "team_id",  # Asumiendo que team_id en teams es string
                "as": "equipo"
            }},
            {"$unwind": "$equipo"},
            
            # 4. Convertir project_id (desde teams) a string
            {"$addFields": {
                "project_id_str": {"$toString": "$equipo.project_id"}  # Asegurar tipo string
            }},
            
            # 5. Agrupar por proyecto sumando personas
            {"$group": {
                "_id": "$project_id_str",
                "totalPersonas": {"$sum": "$totalPersonas"}
            }},
            
            # 6. Unir con proyectos (project_id como string)
            {"$lookup": {
                "from": "projects",
                "localField": "_id",
                "foreignField": "project_id",  # project_id en projects es string
                "as": "proyecto"
            }},
            {"$unwind": "$proyecto"},
            
            # 7. Proyectar campos requeridos
            {"$project": {
                "_id": 0,
                "project_id": "$_id",
                "nombre": "$proyecto.name",
                "location_id": "$proyecto.location_id",
                "totalPersonas": 1
            }},
            
            # 8. Ordenar y obtener el máximo
            {"$sort": {"totalPersonas": -1}},
            {"$limit": 1}
        ]
        
        return list(self.db["works_in_team"].aggregate(pipeline))


    # Saca a traves del id el pokemon favorito de cada persona
    def consulta9_v2(self, person_id):
        query = {
            "person_id": {"$eq": int(person_id)}  # Asegura que sea un entero
        }
        projection = {
            "_id": 0,
            "person_id": 1,
            "pokemon_id": 1
        }
        result = list(self.db["favourite_pokemon"].find(query, projection))
        return result

    # Devuelve las localizaciones
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

