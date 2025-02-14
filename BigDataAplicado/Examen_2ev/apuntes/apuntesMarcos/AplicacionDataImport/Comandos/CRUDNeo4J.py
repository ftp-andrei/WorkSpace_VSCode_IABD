# docker run --name MySQLContainer -v VolumenMySQLContainer:/var/lib/mysql -p 4000:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql
# docker run --name MongoContainer -e MONGO_INITDB_ROOT_USERNAME=MarcosDB -e MONGO_INITDB_ROOT_PASSWORD=secreta -p 6969:27017 -v VolumenMongoContainer:/data/db -d mongo
# docker run  --name Neo4JContainer  --publish=7000:7474 --publish=8000:7687 --env NEO4J_AUTH=neo4j/MySecretPassword --volume VolumenNeo4JContainer:/data -d neo4j

from neo4j import GraphDatabase
import json


class Neo4jCRUD:

    def __init__(self):
        self.nc= ComandosNeo4J('bolt://localhost:8000', 'neo4j', 'MySecretPassword')
        self.nc._connect()
    def crearNodos(self, nombre, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)  # Leer el archivo JSON como una lista de diccionarios
            for item in data:
                # Crear un nodo con todos los parámetros del objeto JSON
                nuevoNodo = {}
                for clave, valor in item.items():
                    nuevoNodo[clave] = valor
                self.nc.create_node(nombre, nuevoNodo)  # Crear el nodo

    
    def crearRelaciones(self, nombreOrigen, valorOrigen, nombreFin, valorFin, nombreRelacion, filename, nombreValorTablaOrigen='id', nombreValorTablaFin='id'):
        # Abrimos el archivo JSON
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)  # Cargamos los datos del archivo JSON

            for item in data:
                propiedades = {}
                valorTablaOrigen = None
                valorTablaFin = None

                # Iteramos sobre las claves y valores del diccionario JSON
                for clave, valor in item.items():
                    # Si la clave no es ni 'valorOrigen' ni 'valorFin', la añadimos a las propiedades
                    if clave != valorOrigen and clave != valorFin:
                        propiedades[clave] = valor

                    # Si la clave es 'valorOrigen', almacenamos el valor correspondiente
                    if clave == valorOrigen:
                        valorTablaOrigen = valor

                    # Si la clave es 'valorFin', almacenamos el valor correspondiente
                    if clave == valorFin:
                        valorTablaFin = valor

                # Crear la relación en la base de datos (o el sistema que estés utilizando)
                self.nc.create_relationship(nombreOrigen, nombreValorTablaOrigen, valorTablaOrigen, nombreFin, nombreValorTablaFin, valorTablaFin, nombreRelacion, propiedades)
    def leerPersonasDeEmpresa(self, nombreEmpresa):
        return self.nc.read_nodes_Ejercicio1(nombreEmpresa)
    def rolesDiferentes(self):
        return self.nc.read_nodes_Ejercicio2()
    def mismaEmpresa(self):
        return self.nc.read_nodes_Ejercicio3()
    def equipoEspecifico(self, idPersonas):
        return self.nc.read_nodes_Ejercicio4(idPersonas)
class ComandosNeo4J:
    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def _connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def create_node(self, label, properties):
        with self._driver.session() as session:
            result = session.execute_write(self._create_node, label, properties)
            return result

    @staticmethod
    def _create_node(tx, label, properties):
        query = (
            f"CREATE (n:{label} $props) "
            "RETURN n"
        )
        result = tx.run(query, props=properties)
        return result.single()[0]

    def create_relationship(self, nombreOrigen, valorOrigen, valorTablaOrigen, nombreFin, valorFin, valorTablaFin, nombreRelacion, propiedades):
        with self._driver.session() as session:
            result = session.execute_write(self._create_relationship, nombreOrigen, valorOrigen, valorTablaOrigen, nombreFin, valorFin, valorTablaFin, nombreRelacion, propiedades)
            return result

    @staticmethod
    def _create_relationship(tx, labelOrigin, propertyOrigin, valuePropertyOrigin, labelEnd, propertyEnd, valuePropertyEnd, relationshipName, properties):
        query = (
        f"MATCH (n:{labelOrigin}), (c:{labelEnd}) "
        f"WHERE n.{propertyOrigin} = $valuePropertyOrigin AND c.{propertyEnd} = $valuePropertyEnd "
        f"CREATE (n)-[r:{relationshipName}]->(c) "
        f"SET r = $properties"
        )

        # Ejecutar la consulta pasando los parámetros
        result = tx.run(query, valuePropertyOrigin=valuePropertyOrigin, valuePropertyEnd=valuePropertyEnd, properties=properties)

        return result
    def read_nodes_Ejercicio1(self, empresa):
        with self._driver.session() as session:
            result = session.execute_write(self._read_nodes_Ejercicio1, empresa)
            return result
    
    @staticmethod
    def _read_nodes_Ejercicio1(tx, empresa):
        query = (
        "MATCH (n:persona)-[t:works_at]->(:empresa {name: $empresa}) "
        "RETURN n, collect(t.rol) AS roles"
        )
        
        # Ejecutamos la consulta con el parámetro 'empresa'
        result = tx.run(query, empresa=empresa)
        return [record.data() for record in result]
    def read_nodes_Ejercicio2(self):
        with self._driver.session() as session:
            result = session.execute_write(self._read_nodes_Ejercicio2)
            return result
    @staticmethod
    def _read_nodes_Ejercicio2(tx):
        query = (
        "MATCH (n:persona)-[t:works_at]->(e:empresa), (m:persona)-[k:works_at]->(z:empresa) "
        "WHERE n <> m AND t.rol = k.rol AND e <> z "
        "RETURN DISTINCT n.name AS persona"
        )
        
        # Ejecutamos la consulta
        result = tx.run(query)
        
        return [record.data() for record in result]
    def read_nodes_Ejercicio3(self):
        with self._driver.session() as session:
            result = session.execute_write(self._read_nodes_Ejercicio3)
            return result
    @staticmethod
    def _read_nodes_Ejercicio3(tx):
        query = (
        "MATCH (n:persona)-[:works_at]->(e:empresa)<-[:works_at]-(m:persona) "
        "WHERE n <> m "
        "RETURN DISTINCT e.name AS empresa"
        )
        
        # Ejecutamos la consulta
        result = tx.run(query)
        
        # Procesamos los resultados y los almacenamos agrupados por rol
        return [record.data() for record in result]


    def read_nodes_Ejercicio4(self, idPersonas):
        with self._driver.session() as session:
            result = session.execute_write(self._read_nodes_Ejercicio4, idPersonas)
            return result
    @staticmethod
    def _read_nodes_Ejercicio4(tx, idPersonas):
        personas = []
        for i in idPersonas:
            query = (
            "MATCH (n:persona {id: $persona}) "
            "RETURN n.id AS idPersona, n.name AS persona"
            )
            
            # Ejecutamos la consulta
            result = tx.run(query, persona= str(i))
            
            # Procesamos los resultados y los almacenamos agrupados por rol
            for record in result:
                personas.append(record["persona"])
        
        return personas