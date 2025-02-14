
from pymongo import MongoClient

from Database.mainNeo4j import Neo4jCRUD

import requests

class MongoDBOperations:
    def __init__(self, database_name, port, username=None, password=None, host="localhost"):
        if username and password:
            self.client = MongoClient(f'mongodb://{username}:{password}@{host}:{port}/')
        else:
            self.client = MongoClient(f'mongodb://{host}:{port}/')
            
        self.db = self.client[database_name]
        self.collection = None
    
    def set_collection(self, collection_name):
        self.collection = self.db[collection_name]
    
    def create_person(self, collection_name, data):
        self.set_collection(collection_name)
        result = self.collection.insert_one(data)
        return result

    def consult(self, collection_name, age):
        self.set_collection(collection_name)
        results = self.collection.find({"age": {"$gt": age}})
        for person in results:
            print(person)

    def fetch_pokemon_data(self, pokenum):
        url = f"https://pokeapi.co/api/v2/pokemon/{pokenum}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                pokemon_info = {
                    "Name": data["name"],
                    "Types": [t["type"]["name"] for t in data["types"]]
                }
                return pokemon_info
            elif response.status_code == 404:
                return f"Pokémon '{pokenum}' not found."
            else:
                return f"Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"

    def consulta41(self, equipo):
        collection = self.db['teams']
        results = collection.find({ "name": equipo }, {"name": 1, "_id": 0, "team_id": 1})

        for person in results:
            print(person['team_id'])

    def consulta4(self, equipo):
        collection = self.db['teams']
        team = collection.find_one({"name": equipo}, {"_id": 0, "team_id": 1})

        team_id = team["team_id"]
        
        collection2 = self.db['works_in_team']
        results = collection2.find({"team_id": team_id}, {"_id": 0, "person_id": 1, "rol": 1})
        return(results)

    def consulta5(self):
        collection = self.db['teams']
        results = collection.find({},{"name": 1, "_id": 0, "team_id": 1})

        for i in results:
            collection2 = self.db['works_in_team']
            nombre=i['name']
            num_personas = collection2.count_documents({"team_id": i['team_id']})
            print(f'· {nombre}: {num_personas} personas.')

    def consulta6(self):
        collection = self.db['teams']
        
        pipeline = [
            {
                "$lookup": {
                    "from": "projects",
                    "localField": "project_id",
                    "foreignField": "project_id",
                    "as": "proyectos"
                }
            },
            {
                "$project": {
                "team_id": 1,
                "name": 1,
                "num_projects": { "$size": "$proyectos" }
                }
            }
        ]
        
        
        results = collection.aggregate(pipeline)

        for i in results:
            print(f'· {i['name']}:  {i['num_projects']} proyectos.')


    def consulta9(self):
        print('Revisando Pokémon...')
        collection = self.db['works_in_team']
        pipeline = [
            {    
                "$addFields": {
                    "person_id_int": { "$toInt": "$person_id" }
                }
            },
            {
                "$lookup": {
                    "from": "favourite_pokemon",
                    "localField": "person_id_int",
                    "foreignField": "person_id",
                    "as": "favpokemon"
                }
            },
            {"$unwind": "$favpokemon"},
            {
                "$group": {
                    "_id": "$team_id",
                    "pokemones": { "$push": "$favpokemon.pokemon_id" }
                }
            }
        ]
        results = collection.aggregate(pipeline)
        equipotipos = {}
        for i in results:
            tipos = []
            for e in i['pokemones']:
                for u in self.fetch_pokemon_data(e)['Types']:
                    if u not in tipos:
                       tipos.append(u) 
            equipotipos[i['_id']] = tipos
            tipos = []

        collection2 = self.db['teams']
        pipeline = [
            {
                "$match": {
                    "team_id": f"{max(equipotipos)}"
                }
            },
            {
                "$lookup": {
                    "from": "projects",
                    "localField": "project_id",
                    "foreignField": "project_id",
                    "as": "proyecto"
                }
            },
            {"$unwind": "$proyecto"},
            {
                "$project": {
                    "_id": 0,
                    "team_id": 1,
                    "project_name": "$proyecto.name"
                }
            }
        ]
        results = collection2.aggregate(pipeline)
        for i in results:
            print(f'El proyecto cuyo equipo posee mayor variedad de tipos dentro de los Pokémon favoritos de sus integrantes es {i['project_name']}. ')
            print(f'Abarcan {len(equipotipos[max(equipotipos)])} tipos distintos, que son: ')
            print(f'{equipotipos[max(equipotipos)]}')
            

    def consulta10(self, loca, uri, user, password):
            collection = self.db['projects']
            pipeline = [
                {
                    "$lookup": {
                        "from": "teams",
                        "localField": "project_id",
                        "foreignField": "project_id",
                        "as": "equipo"
                    }
                },
                {
                    "$match": {
                        "location_id": f"{loca}"
                    }
                }
            ]
            
            for i in collection.aggregate(pipeline):
                print(f'Proyecto: {i['name']}')
                print('     Equipos:')
                if(len(i['equipo']))==0:
                    print(f'        -No se han encontrado equipos-')
                for e in i['equipo']:
                    collection2 = self.db['works_in_team']
                    print(f'        {e['name']}:')
                    pipetemp=[
                        {
                            "$match": {
                                "team_id": f"{e['team_id']}"
                            }
                        }
                    ]
                    for u in collection2.aggregate(pipetemp):
                        neo4j = Neo4jCRUD(uri, user, password)
                        laburador = neo4j.consulta10(u['person_id'])
                        for u in laburador:
                            print(f"            · {u[0]}: {u[1]} años.")
                print('---------------------------------------------------')