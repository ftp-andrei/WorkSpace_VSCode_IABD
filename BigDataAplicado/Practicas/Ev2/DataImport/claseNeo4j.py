from neo4j import GraphDatabase
import csv

# TODO: Falta relacion entre los 2 nodos

# Función para leer archivos CSV
def read_csv_file(filename):
    data =[]
    with open(filename, 'r',encoding="utf-8") as file:
        reader= csv.reader(file)
        next(reader)  # Saltar la cabecera
        for element in reader:
            data.append(element)        
    return data

class Neo4J:
    def __init__(self, uri, user, password):

        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None
        self._connect()

    # Conectar a la bd
    def _connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
        print("Conexión a Neo4j exitosa.")

    # Cerrar conexion
    def close(self):
        if self._driver is not None:
            self._driver.close()

    # Crear nodos
    def create_node(self, label, properties):
        with self._driver.session() as session:
            result = session.write_transaction(self._create_node, label, properties)
            return result

    @staticmethod
    def _create_node(tx, label, properties):
        query = (
            f"CREATE (n:{label} $props)"
        )
        result = tx.run(query, props=properties)
        return result

    # Crear relaciones
    def create_relationship(self,label_origin, property_origin, label_end, property_end, relationship_name):
        with self._driver.session() as session:
            result = session.write_transaction(
                self._create_relationship,
                label_origin,
                property_origin,
                label_end,
                property_end,
                relationship_name
            )
            return result
        
    @staticmethod
    def _create_relationship(tx, label_origin, property_origin, label_end, property_end, relationship_name):
        query = (
            f"MATCH (a:{label_origin}), (b:{label_end}) "
            f"CREATE (a)-[:{relationship_name}]->(b)"
        )
        result= tx.run(query, property_origin=property_origin, property_end=property_end)
        return result
    
    # Obtener personas que trabajan en una empresa
    def consulta1(self, empresa_name):
        with self._driver.session() as session:
            result = session.read_transaction(self._consulta1, empresa_name)
            for record in result:
                print(f"Persona: {record['persona']}, Empresa: {record['empresa']}, Location ID: {record['location_id']}, Rol: {record['rol']}")

    @staticmethod
    def _consulta1(tx, empresa_name):
        query = """
            MATCH (p:Persona)-[r:WORKS_AT]->(e:Empresa)
            WHERE e.name = $empresa_name
            RETURN p.name AS persona, e.name AS empresa, r.location_id AS location_id, r.role AS rol
        """
        return tx.run(query, empresa_name=empresa_name)

uri = "bolt://localhost:7687" 
user = "neo4j"
password = "my-secret-pw"

neo4j_crud = Neo4J(uri, user, password)

empresas= read_csv_file("Archivos/Neo4J/empresas.csv")
persons=read_csv_file("Archivos/Neo4J/persons.csv")
works_at=read_csv_file("Archivos/Neo4J/works_at.csv")

# Crear nodos de Empresa
for element in empresas[1:]:
    node_properties = {
        "id": element[0],
        "name": element[1],
        "sector": element[2]
    }
    neo4j_crud.create_node("Empresa", node_properties)

# Crear nodos de Persona
for element in persons[1:]:
    node_properties = {
        "id": element[0],
        "name": element[1],
        "age": element[2]
    }
    neo4j_crud.create_node("Persona", node_properties)

# Crear relacion WORKS_AT
for element in works_at[1:]:
    # Llamada a la función create_relationship
    neo4j_crud.create_relationship(
        "Persona",   # labelOrigin
        element[0],  # persona_id (propertyOrigin)
        "Empresa",   # labelEnd
        element[2],  # empresa_id (propertyEnd)
        "WORKS_AT"   # relationshipName
    )
