from neo4j import GraphDatabase

'''
MATCH (n:Empresas)
DETACH DELETE n

MATCH (n:Persons)
DETACH DELETE n
'''


class Neo4jCRUD:
    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None
        self._connect()

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
        

    def consulta1(self, empresa):
        with self._driver.session() as session:
            return session.execute_write(self._consulta1, empresa)
          
    @staticmethod
    def _consulta1(tx, empresa):
        query = (
            f"MATCH (n:Persons)-[r]-(v:Empresas) where v.name='{empresa}' RETURN n.name,r.rol"
        )
        result = tx.run(query)
        return [record for record in result]
    
    def consulta2(self):
        with self._driver.session() as session:
            return session.execute_write(self._consulta2)
        
    @staticmethod
    def _consulta2(tx):
        query = (
            "MATCH (v2:Empresas)<-[r2]-(n:Persons)-[r]->(v:Empresas) "
            "WHERE r.rol = r2.rol "
            "RETURN n.name, r.rol, v.name, v2.name"
        )
        result = tx.run(query)
        return [record for record in result]
    
    def consulta3(self, per1, per2):
        with self._driver.session() as session:
            return session.execute_write(self._consulta3, per1, per2)
          
    @staticmethod
    def _consulta3(tx, per1, per2):
        query = (
            f"MATCH (p:Persons)-[r]->(e:Empresas)<-[r2]-(p2:Persons) where p.name='{per1}' AND p2.name='{per2}' RETURN DISTINCT e.name"
        )
        result = tx.run(query)
        return [record for record in result]
    
    def consulta4(self, lista):
        with self._driver.session() as session:
            return session.execute_write(self._consulta4, lista)
          
    @staticmethod
    def _consulta4(tx, per):
            query = (
                f"MATCH (p:Persons) where p.id = '{per}' RETURN p.name"
            )
            result = tx.run(query)
            return [record for record in result]
    
    def consulta10(self, lista):
        with self._driver.session() as session:
            return session.execute_write(self._consulta10, lista)
          
    @staticmethod
    def _consulta10(tx, per):
            query = (
                f"MATCH (p:Persons) where p.id = '{per}' RETURN p.name, p.age"
            )
            result = tx.run(query)
            return [record for record in result]

            
    
    def create_relationship(self,labelOrigin,propertyOrigin,labelEnd,propertyEnd,relationshipName,rol):
         with self._driver.session() as session:
            result = session.execute_write(self._create_relationship, labelOrigin,propertyOrigin,labelEnd,propertyEnd,relationshipName,rol)
            return result
        
    @staticmethod
    def _create_relationship(tx, labelOrigin,propertyOrigin,labelEnd,propertyEnd,relationshipName,rol):
        query = (
            f"MATCH (n:{labelOrigin}),(c:{labelEnd}) "
            f"WHERE n.id='{propertyOrigin}' and c.id='{propertyEnd}' " 
            f"CREATE (n)-[:{relationshipName} {{rol:'{rol}'}} ]->(c)"
        )
        result = tx.run(query)
        return result


