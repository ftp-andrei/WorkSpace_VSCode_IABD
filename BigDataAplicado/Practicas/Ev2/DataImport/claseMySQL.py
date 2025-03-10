import csv
import json
import mysql.connector

# Creacion de tablas 
create_table_has_skill = """
        CREATE TABLE IF NOT EXISTS Has_Skill (
            id INT AUTO_INCREMENT PRIMARY KEY,
            person_id INT,
            skill_id INT,
            proficiency VARCHAR(255),
            FOREIGN KEY (skill_id) REFERENCES Skills(id) ON DELETE CASCADE ON UPDATE CASCADE
        );
        """    

create_table_locations = """
        CREATE TABLE IF NOT EXISTS Locations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            city VARCHAR(255)
        );
        """    

create_table_pokemon = """
        CREATE TABLE IF NOT EXISTS Pokemon (
            pokemon_id INT PRIMARY KEY,
            description VARCHAR(255),
            pokeGame VARCHAR(255)
        );
        """        
        
create_table_skills = """
        CREATE TABLE IF NOT EXISTS Skills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255)
        );
        """

def json_to_csv(json_file, csv_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as file_json:
            data = json.load(file_json)

        if not data:
            print("El archivo JSON está vacío.")
            return
        
        # Escribir los datos en un archivo CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as file_csv:
            writer = csv.DictWriter(file_csv, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Archivo CSV generado: {csv_file}")
    
    except Exception as e:
        print(f"Error: {e}")

class MySQL:
    def __init__(self, host, user, password, database,port):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            #database=database,
            port=port
        )

        # Creando el cursor
        self.cursor = self.connection.cursor()

        # Crear la base de datos solo si no existe
        self.create_database(database)

        # Conectarse a la base de datos especificada
        self.connection.database = database

    def create_database(self, database_name):
        # Comprobamos si la base de datos existe
        self.cursor.execute(f"SHOW DATABASES LIKE '{database_name}';")
        # Devuelve el 1er resultado
        result = self.cursor.fetchone()
        
        if result:
            print(f"MySQL: La base de datos '{database_name}' ya existe.")
        else:
            # Si no existe, la creamos
            self.cursor.execute(f"CREATE DATABASE {database_name};")
            print(f"MySQL: Base de datos '{database_name}' creada.")

    def create_table(self,stringCreate):
        self.cursor.execute(stringCreate)
        self.connection.commit()

    def insert_data(self, query,params):
        self.cursor.execute(query, params)
        self.connection.commit()
    
    def close(self):
        if self.connection is not None:
            self.cursor.close()
            self.connection.close()

#------------------CONSULTAS-------------------------

    # Obtener todas las skills en las que una persona tiene al menos un nivel específico de proficiency
    def consulta7(self, persona_id, proficiency):
        # Definir la consulta
        query = "SELECT hs.skill_id, hs.proficiency FROM Has_Skill hs WHERE hs.person_id = %s AND hs.proficiency = %s"

        # Ejecutar la consulta
        self.cursor.execute(query, (persona_id, proficiency))

        # Obtener y mostrar los resultados
        results = self.cursor.fetchall()
        return results
    
    # Encontrar todas las personas que tienen skill en al menos una skill en común con otra persona (es decir, encontrar personas con skills similares).
    def consulta8(self):
        query = """
            SELECT DISTINCT h1.person_id AS person1_id, h2.person_id AS person2_id
            FROM Has_Skill h1
            JOIN Has_Skill h2 ON h1.skill_id = h2.skill_id
            WHERE h1.person_id < h2.person_id;
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    # Dado una ubicación, obtén la lista de equipos que están ubicados allí junto con información de las personas que trabajan en ese equipo y los proyectos asociados
    def consulta10(self):
        query = """
            SELECT id, name FROM Locations;
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

#---------------------------------------------

# Archivos JSON a CSV
json_to_csv("Archivos/MySQL/has_skill.json", "Archivos/MySQL/has_skill.csv")
json_to_csv("Archivos/MySQL/locations.json", "Archivos/MySQL/locations.csv")
json_to_csv("Archivos/MySQL/pokemon.json", "Archivos/MySQL/pokemon.csv")
json_to_csv("Archivos/MySQL/skills.json", "Archivos/MySQL/skills.csv")

def read_csv_file(filename):
    data =[]
    with open(filename, 'r') as file:
        reader= csv.reader(file)
        for element in reader:
            data.append(element)        
    return data

# Lectura ficheros
has_skill= read_csv_file("Archivos/MySQL/has_skill.csv")
locations=read_csv_file("Archivos/MySQL/locations.csv")
pokemon=read_csv_file("Archivos/MySQL/pokemon.csv")
skills=read_csv_file("Archivos/MySQL/skills.csv")

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "my-secret-pw"
DB_DATABASE = "PokemonDB" 
DB_PORT= 6969

db = MySQL(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE,DB_PORT)
# Creamos las tablas
db.create_table(create_table_skills)
db.create_table(create_table_has_skill)
db.create_table(create_table_locations)
db.create_table(create_table_pokemon)


#-----------INSERTAMOS DATOS---------------

# Para Skills
for element in skills[1:]:
    # Verificar si ya existe el registro
    select_query = "SELECT COUNT(*) FROM Skills WHERE name = %s"
    db.cursor.execute(select_query, (element[1],))
    result = db.cursor.fetchone()
    
    # Si no existe, lo insertamos
    if result[0] == 0:
        insert_query = "INSERT INTO Skills (name) VALUES (%s)"
        db.insert_data(insert_query, (element[1],))

# Para Has_Skill
for element in has_skill[1:]:
    # Verificar si ya existe el registro
    select_query = "SELECT COUNT(*) FROM Has_Skill WHERE person_id = %s AND skill_id = %s"
    db.cursor.execute(select_query, (element[0], element[1]))
    result = db.cursor.fetchone()
    
    # Si no existe, lo insertamos
    if result[0] == 0:
        insert_query = "INSERT INTO Has_Skill (person_id, skill_id, proficiency) VALUES (%s, %s, %s)"
        db.insert_data(insert_query, (element[0], element[1], element[2]))

# Para Locations
for element in locations[1:]:
    # Verificar si ya existe el registro
    select_query = "SELECT COUNT(*) FROM Locations WHERE id = %s"
    db.cursor.execute(select_query, (element[0],))
    result = db.cursor.fetchone()
    
    # Si no existe, lo insertamos
    if result[0] == 0:
        insert_query = "INSERT INTO Locations (id, name, city) VALUES (%s, %s, %s)"
        db.insert_data(insert_query, (element[0], element[1], element[2]))

# Para Pokemon
for element in pokemon[1:]:
    # Verificar si ya existe el registro
    select_query = "SELECT COUNT(*) FROM Pokemon WHERE pokemon_id = %s"
    db.cursor.execute(select_query, (element[0],))
    result = db.cursor.fetchone()
    
    # Si no existe, lo insertamos
    if result[0] == 0:
        insert_query = "INSERT INTO Pokemon (pokemon_id, description, pokeGame) VALUES (%s, %s, %s)"
        db.insert_data(insert_query, (element[0], element[1], element[2]))
print("MySQL: Datos insertados correctamente.") 