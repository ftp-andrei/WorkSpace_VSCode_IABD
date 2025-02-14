
import csv

from Database.mainNeo4j import Neo4jCRUD

def read_csv_file(filename):
    data =[]
    with open(filename, 'r',encoding="utf-8") as file:
        reader= csv.reader(file)
        for element in reader:
            data.append(element)        
    return data

uri = "bolt://localhost:7687"  
user = "neo4j"
password = "password"
neo4j_crud = Neo4jCRUD(uri, user, password)

readerEmpresas = read_csv_file("neo4j/empresas.csv")
readerPersons = read_csv_file("neo4j/persons.csv")
readerWorksat = read_csv_file("neo4j/works_at.csv")

for element in readerEmpresas[1:]:
    node_properties = {
        "id": element[0], 
        "name": element[1],
        "sector": element[2]
    }
    neo4j_crud.create_node("Empresas", node_properties)

for element in readerPersons[1:]:
    node_properties = {
        "id": element[0], 
        "name": element[1],
        "age": element[2]
    }
    neo4j_crud.create_node("Persons", node_properties)


for element in readerWorksat[1:]:
    neo4j_crud.create_relationship("Persons", element[0], "Empresas", element[2], "TRABAJA", element[1])

neo4j_crud.close()


