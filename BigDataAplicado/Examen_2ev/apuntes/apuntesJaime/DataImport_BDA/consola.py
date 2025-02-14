from Database.mainMySQL import Database
from Database.mainNeo4j import Neo4jCRUD
from Database.mainMongo import MongoDBOperations

uri = "bolt://localhost:7687"  
user = "neo4j"
password = "password"
neo4j = Neo4jCRUD(uri, user, password)


DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "my-secret-pw"
DB_DATABASE = "Trafabajo"
DB_PORT= "6969"
db = Database(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE,DB_PORT)

MONGO_DATABASE = "Trafabajo2"
MONGO_PORT = "7777"
MONGO_USER = "mongoadmin"
MONGO_PASSWORD = "secret"

mongo = MongoDBOperations(MONGO_DATABASE, MONGO_PORT, MONGO_USER, MONGO_PASSWORD)

while True:
    print("\nMenu:")
    print("1. Personas y sus roles en una empresa concreta.")
    print("2. Personas con el mismo rol en diferentes empresas.")
    print("3. Empresas comunes entre dos personas.")
    print("4. Personas y sus funciones en un equipo específico.")
    print("5. Muestra todos los equipos con el número de personas que los componen.")
    print("6. Muestra los equipos con el número total de proyectos a los que están asociados")
    print("7. Obtener todas las skills en las que una persona tiene al menos un nivel específico de proficiency.")
    print("8. Encontrar todas las personas que tienen skill en al menos una skill en común con otra persona (es decir, encontrar personas con skills similares).")
    print("9. Encontrar el proyecto que tenga más personas en el equipo cuyos pokemons favoritos son de diferente tipo, mostrar todo los tipos distintos.")
    print("10. Dado una ubicación, obtén la lista de equipos que están ubicados allí junto con información de las personas que trabajan en ese equipo y los proyectos asociados.")
    choice = input("Enter your choice (1/2/3/4/5/6/7/8/9/10): ")
    
    if choice == '1':
        consul1=neo4j.consulta1(input('Introduzca el nombre de una empresa. [Ej: Company_4]: '))
        for producto in consul1:
            print(f'{producto[0]} {producto[1]}')
        
    elif choice == '2':
        consul2=neo4j.consulta2()
        for producto in consul2:
            print(f'{producto[0]} posee el puesto de {producto[1]} tanto en {producto[2]} como en {producto[3]}')

    elif choice == '3':
        consul3=neo4j.consulta3(input('Introduzca el nombre de una persona. [Ej: Person_20]: '), input('Introduzca el nombre de una persona. [Ej: Person_27]: '))
        for producto in consul3:
            print(f'{producto[0]}')

    elif choice == '4':
        consul4=mongo.consulta4(input('Introduzca el nombre de un equipo. [Ej: Team_2]: '))
        
        for i in consul4:
            perid = i["person_id"]
            rol = i["rol"]
            
            nombre = neo4j.consulta4(perid)
            for producto in nombre:
                print(f"· {producto[0]}: {rol}")

    elif choice == '5':
        mongo.consulta5()

    elif choice == '6':
        mongo.consulta6()

    elif choice == '7':
        accu=input('Introduzca un nivel de profficiency. [Ej: Beginner]: ')
        result=db.consulta7(accu)
        for i in result:
            nombre = neo4j.consulta4(i[1])
            for producto in nombre:
                print(f"· {producto[0]}: es {accu} en {i[0]}")

    elif choice == '8':
        result=db.consulta8()
        for i in result:
            nombre1 = neo4j.consulta4(i[0])
            nombre2 = neo4j.consulta4(i[1])
            for producto in nombre1:
                nom1= producto[0]
            for producto in nombre2:
                nom2= producto[0]
            print(f'{nom1} y {nom2} comparten {i[2]}')


    elif choice == '9':
        mongo.consulta9()

    elif choice == '10':
        loc=db.consulta10(input('Introduzca el nombre de una localización. [Ej: Location_6]: '))
        mongo.consulta10(loc[0], uri, user, password)

    else:
        print("Invalid choice. Please select a valid option.")
