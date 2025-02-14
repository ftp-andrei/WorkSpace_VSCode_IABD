import csv

from Database.mainMySQL import Database

def main():
    create_table_queryLocations = """
            CREATE TABLE IF NOT EXISTS Locations (
                id INT PRIMARY KEY,
                name VARCHAR(255),
                city VARCHAR(255)
            )
            """
            
    create_table_querySkills = """
            CREATE TABLE IF NOT EXISTS Skills (
                id INT PRIMARY KEY,
                name VARCHAR(255)
            )
            """
            
    create_table_queryPokemon = """
            CREATE TABLE IF NOT EXISTS Pokemon (
                pokemon_id INT PRIMARY KEY,
                description VARCHAR(255),
                pokeGame VARCHAR(255)
            )
            """        

    create_table_queryHas_skill = """
            CREATE TABLE IF NOT EXISTS Has_skill (
                id INT PRIMARY KEY AUTO_INCREMENT,
                person_id INT,
                skill_id INT,
                proficiency VARCHAR(255)
            )
            """  

    def read_csv_file(filename):
        data =[]
        with open(filename, 'r') as file:
            reader= csv.reader(file)
            for element in reader:
                data.append(element)        
        return data
        
    readerLocations= read_csv_file("mysql/locations.csv")
    readerSkills=read_csv_file("mysql/skills.csv")
    readerPokemon=read_csv_file("mysql/pokemon.csv")
    readerHas_Skills=read_csv_file("mysql/has_skill.csv")

    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = "my-secret-pw"
    DB_DATABASE = "Trafabajo"
    DB_PORT= "6969"

    db = Database(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE,DB_PORT)
    db.create_table(create_table_queryLocations)
    db.create_table(create_table_querySkills)
    db.create_table(create_table_queryPokemon)
    db.create_table(create_table_queryHas_skill)

            
    for element in readerLocations[1:]:
        insert_query = "INSERT INTO Locations (id, name,city) VALUES (%s, %s, %s)"
        data= (element[0],element[1],element[2])
        db.insert_data(insert_query,data)
        
    for element in readerSkills[1:]:
        insert_query = "INSERT INTO Skills (id, name) VALUES (%s, %s)"
        data= (element[0],element[1])
        db.insert_data(insert_query,data)
        
    for element in readerPokemon[1:]:
        insert_query = "INSERT INTO Pokemon (pokemon_id, description,pokeGame) VALUES (%s, %s, %s)"
        data= (element[0],element[1],element[2])
        db.insert_data(insert_query,data)

    for element in readerHas_Skills[1:]:
        insert_query = "INSERT INTO Has_skill (person_id,skill_id,proficiency) VALUES (%s, %s, %s)"
        data= (element[0],element[1],element[2])
        db.insert_data(insert_query,data)
if __name__ == "__main__":
    main()