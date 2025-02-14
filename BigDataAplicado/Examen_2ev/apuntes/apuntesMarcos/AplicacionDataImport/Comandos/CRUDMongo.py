# docker run --name MySQLContainer -v VolumenMySQLContainer:/var/lib/mysql -p 4000:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql
# docker run --name MongoContainer -e MONGO_INITDB_ROOT_USERNAME=MarcosDB -e MONGO_INITDB_ROOT_PASSWORD=secreta -p 6969:27017 -v VolumenMongoContainer:/data/db -d mongo
# docker run  --name Neo4JContainer  --publish=7000:7474 --publish=8000:7687 --env NEO4J_AUTH=neo4j/MySecretPassword --volume VolumenNeo4JContainer:/data -d neo4j

from pymongo import MongoClient
import json

class MongoCRUD:

    def __init__(self):
        self.client = MongoClient('mongodb://MarcosDB:secreta@localhost:6969/')
        self.db = self.client['mongoDB']
        self.mc= ComandosMongoDB(self.db)

    def crearColeccion(self, filename, collection_name):

        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                self.mc.create_Collection(collection_name, item)
    
    def nuevoDato(self, filename, attribute_name, id_name, collection_name, id_tabla_original):
        """
        Agrega un nuevo atributo (un array) a los registros correspondientes en la base de datos,
        basado en la relación indicada en el archivo JSON.

        Args:
            filename (str): Ruta del archivo JSON que contiene los datos de las personas.
            attribute_name (str): Nombre del nuevo atributo que se agregará a los registros.
            id_name (str): Nombre del atributo en el archivo JSON que indica a qué registro pertenece.
            collection_name (str): Nombre de la colección en MongoDB.
        """
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Organizar los datos por id_name
        grouped_data = {}
        for item in data:
            key = item[id_name]
            if key not in grouped_data:
                grouped_data[key] = []

            # Quitar el atributo `id_name` del objeto antes de añadirlo al array
            filtered_item = {k: v for k, v in item.items() if k != id_name}
            grouped_data[key].append(filtered_item)

        # Realizar la actualización de los registros en la base de datos
        self.mc.update_Collection(collection_name, grouped_data, attribute_name, id_tabla_original)
    def generarPipeline(self, pipeline):
        return self.mc.aggregation_pipeline(pipeline)


class ComandosMongoDB:
    def __init__(self, database):
        self.db= database

    
    def create_Collection(self, collection_name, modelo):
        self.collection = self.db[collection_name]
        result = self.collection.insert_one(modelo)
        return result
    def update_Collection(self, collection_name, grouped_data, attribute_name, id_tabla_original):
        self.collection = self.db[collection_name]
        for key, values in grouped_data.items():
            result = self.collection.update_one(
                {id_tabla_original: key},  # Buscar el documento con el id correspondiente
                {"$set": {attribute_name: values}}  # Agregar o actualizar el nuevo atributo
            )
            # Mostrar información sobre los cambios realizados
            if result.modified_count > 0:
                print(f"Modificado registro con id={key}, atributo '{attribute_name}' actualizado.")
            else:
                print(f"No se encontró registro con id={key}, no se realizó ningún cambio.")

    def aggregation_pipeline(self, pipeline):
        coleccionNueva = self.db['equipos']
        result = coleccionNueva.aggregate(pipeline)
        return result