import mysql.connector

class Database:
    def __init__(self, host, user, password, database,port):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            port=port,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def create_table(self,stringCreate):
        self.cursor.execute(stringCreate)
        self.connection.commit()

    def insert_data(self, query,params):
        self.cursor.execute(query, params)
        self.connection.commit()
    
    def get_all_data(self):
        select_all_query = "SELECT * FROM Partido"
        self.cursor.execute(select_all_query)
        result = self.cursor.fetchall()
        partidos = []
        for row in result:
            partido = (row[1], row[2], row[3], row[0])  
            partidos.append(partido)
        return partidos
    
    def consulta7(self, accu):
        query = f"SELECT s.name, h.person_id FROM Skills s LEFT JOIN Has_skill h ON h.skill_id = s.id WHERE h.proficiency >= '{accu}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return(result)


    def consulta8(self):
        query = "SELECT DISTINCT hs1.person_id AS per1, hs2.person_id AS per2, s.name FROM Has_skill hs1 JOIN Has_skill hs2 ON hs1.skill_id = hs2.skill_id AND hs1.person_id != hs2.person_id JOIN Skills s ON hs1.skill_id = s.id ORDER BY per1, per2"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return(result)

    def consulta10(self, loc):
        query = f"SELECT id FROM Locations WHERE name LIKE '{loc}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result[0]

        
            
            
