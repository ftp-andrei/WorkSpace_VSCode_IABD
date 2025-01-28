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

    # Cerrar conexion
    def close(self):
        if self._driver is not None:
            self._driver.close()

    # Eliminar nodos - relaciones
    def eliminar_todos_los_nodos_y_relaciones(self):
        with self._driver.session() as session:
            result = session.execute_write(self._eliminar_todos_los_nodos_y_relaciones)
            return result

    @staticmethod
    def _eliminar_todos_los_nodos_y_relaciones(tx):
        query = """
            MATCH (n)
            RETURN COUNT(n) AS total_nodos
        """
        result = tx.run(query)
        total_nodos = result.single()["total_nodos"]

        if total_nodos > 0:
            # Si existen nodos, los eliminamos
            query_delete = """
                MATCH (n)
                DETACH DELETE n
            """
            tx.run(query_delete)
            print(f"Se han eliminado {total_nodos} nodos y sus relaciones.")
        else:
            print("No existen nodos para eliminar.")

    # Crear nodos
    def create_node(self, label, properties):
        with self._driver.session() as session:
            result = session.execute_write(self._create_node, label, properties)
            return result

    @staticmethod
    def _create_node(tx, label, properties):
        query = (
            f"CREATE (n:{label} $props)"
        )
        result = tx.run(query, props=properties)
        return result

    # Crear relaciones
    def create_relationship_with_role(self, label_origin, property_origin, label_end, property_end, relationship_name, role):
        with self._driver.session() as session:
            result = session.execute_write(
                self._create_relationship_with_role,
                label_origin,
                property_origin,
                label_end,
                property_end,
                relationship_name,
                role
            )
            return result
        
    @staticmethod
    def _create_relationship_with_role(tx, label_origin, property_origin, label_end, property_end, relationship_name, role):
        query = (
            f"MATCH (a:{label_origin} {{id: $property_origin}}), (b:{label_end} {{id: $property_end}}) "
            f"MERGE (a)-[r:{relationship_name}]->(b) "  # Asegura que no se creen relaciones duplicadas (Se puede cambiar por CREATE)
            f"ON CREATE SET r.role = $role "            # Establece la propiedad `role` solo si la relación es nueva
        )
        result = tx.run(query, property_origin=property_origin, property_end=property_end, role=role)
        return result

#----------------CONSULTAS----------------

    # Personas y sus roles en una empresa concreta
    def consulta1(self, empresa_name):
        with self._driver.session() as session:
            # Ejecutar la consulta y obtener los resultados en la transacción
            result = session.execute_read(self._consulta1, empresa_name)
            return result

    @staticmethod
    def _consulta1(tx, empresa_name):
        query = """
            MATCH (p:Persona)-[r:WORKS_AT]->(e:Empresa)
            WHERE e.name = $empresa_name
            RETURN p.name AS persona, r.role AS rol
        """
        result =  tx.run(query, empresa_name=empresa_name)

        for record in result:
            print(f"Persona: {record['persona']}, Rol: {record['rol']}")

    # Personas con el mismo rol en diferentes empresas
    def consulta2(self):
        with self._driver.session() as session:
            result = session.execute_read(self._consulta2)
            return result

    @staticmethod
    def _consulta2(tx):
        query = """
            MATCH (p:Persona)-[r:WORKS_AT]->(e:Empresa)
            WITH p, r.role AS rol, COLLECT(e.name) AS empresas
            WHERE SIZE(empresas) > 1  
            RETURN p.name AS persona, rol, empresas
        """
        result =  tx.run(query)

        for record in result:
            print(f"Persona: {record['persona']}, Rol: {record['rol']}, Empresas: {record['empresas']}")

    # Empresas comunes entre dos personas
    def consulta3(self):
        with self._driver.session() as session:
            result = session.execute_read(self._consulta3)
            return result

    @staticmethod
    def _consulta3(tx):
        query = """
            MATCH (p1:Persona)-[:WORKS_AT]->(e:Empresa)<-[:WORKS_AT]-(p2:Persona)
            WHERE p1 <> p2  
            RETURN p1.name AS persona1, p2.name AS persona2, e.name AS empresa_comun
        """
        # <> | Asegura que no se comparen la misma persona consigo misma
        result = tx.run(query)

        for record in result:
            print(f"Persona 1: {record['persona1']}, Persona 2: {record['persona2']}, Empresa común: {record['empresa_comun']}")

    # Obtener todas las skills en las que una persona tiene al menos un nivel específico de proficiency
    def consulta7(self):
        with self._driver.session() as session:
            result = session.execute_read(self._consulta7)
            return result
    
    def _consulta7(self,tx):
        query = """
             MATCH (p:Persona)
             RETURN p.id AS person_id, p.name AS person_name
        """
        result = tx.run(query)
        data = []

        for record in result:
            person = {
                "id": record["person_id"],
                "name": record["person_name"]
            }
            data.append(person)

        return data

        # Construir una lista con los resultados
        #return [{"id": record["person_id"], "name": record["person_name"]} for record in result]

#-----------------------------------

uri = "bolt://localhost:7687" 
user = "neo4j"
password = "my-secret-pw"

neo4j_crud = Neo4J(uri, user, password)

# Eliminamos por si estan creados
neo4j_crud.eliminar_todos_los_nodos_y_relaciones()

empresas = read_csv_file("Archivos/Neo4J/empresas.csv")
persons = read_csv_file("Archivos/Neo4J/persons.csv")
works_at = read_csv_file("Archivos/Neo4J/works_at.csv")

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
    neo4j_crud.create_relationship_with_role(
        "Persona",   # labelOrigin
        element[0],  # persona_id (propertyOrigin)
        "Empresa",   # labelEnd
        element[2],  # empresa_id (propertyEnd)
        "WORKS_AT",  # relationshipName
        element[1]   # role
    )
print("Neo: Datos insertados correctamente.") 