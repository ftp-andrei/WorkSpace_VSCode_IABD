import csv
import mysql.connector
# pip install mysql-connector-python


# Creacion de tablas 
# Añadir estructura ficheros 

create_table_queryCars = """
        CREATE TABLE IF NOT EXISTS Cars (
            id INT PRIMARY KEY,
            brand VARCHAR(255),
            model VARCHAR(255),
            year INT
        )
        """
        
create_table_queryRentals = """
        CREATE TABLE IF NOT EXISTS Rentals (
            id INT PRIMARY KEY,
            car_id INT,
            customer_id INT,
            rental_date datetime
        )
        """
        
create_table_queryCustomers = """
        CREATE TABLE IF NOT EXISTS Customers (
            id INT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255)
        )
        """        

def read_csv_file(filename):
    data =[]
    with open(filename, 'r') as file:
        reader= csv.reader(file)
        for element in reader:
            data.append(element)        
    return data

class MySQL:
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
        
            
            
has_skill= read_csv_file("Archivos/MySQL/has_skill.csv")
locations=read_csv_file("Archivos/MySQL/locations.csv")
pokemon=read_csv_file("Archivos/MySQL/pokemon.csv")
skills=read_csv_file("Archivos/MySQL/skills.csv")

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "my-secret-pw"
DB_DATABASE = "Coches" # Cambiar nombre
DB_PORT= "8888" # Cambiar puerto (6969:3306)

db = MySQL(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE,DB_PORT)
db.create_table(create_table_queryCars)
db.create_table(create_table_queryRentals)
db.create_table(create_table_queryCustomers)

        
# for element in readerCars[1:]:
#     insert_query = "INSERT INTO Cars (id, brand,model,year) VALUES (%s, %s, %s, %s)"
#     data= (element[0],element[1],element[2],element[3])
#     db.insert_data(insert_query,data)
    
# for element in readerRentals[1:]:
#     insert_query = "INSERT INTO Rentals (id, car_id,customer_id,rental_date) VALUES (%s, %s, %s, %s)"
#     data= (element[0],element[1],element[2],element[3])
#     db.insert_data(insert_query,data)
    
# for element in readerCustomers[1:]:
#     insert_query = "INSERT INTO Customers (id, name,email) VALUES (%s, %s, %s)"
#     data= (element[0],element[1],element[2])
#     db.insert_data(insert_query,data)