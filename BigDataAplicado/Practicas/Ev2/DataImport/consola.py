from claseNeo4j import Neo4J
from claseMongoDB import MongoDB
from claseMySQL import MySQL

def connect_to_neo4j():
    neo_uri = "bolt://localhost:7687"
    neo_user = "neo4j"
    neo_password = "my-secret-pw"
    neo4j = Neo4J(neo_uri, neo_user, neo_password)
    print("Conexión a Neo4j establecida.")
    return neo4j

def connect_to_mongodb():
    mongodb_database_name = "PokemonDB"
    mongodb_port = 27017
    mongodb = MongoDB(mongodb_database_name, mongodb_port, username='mongoadmin', password='secret')
    print("Conexión a MongoDB establecida.")
    return mongodb

def connect_to_mysql():
    mysql_host = "localhost"
    mysql_user = "root"
    mysql_password = "my-secret-pw"
    mysql_database = "PokemonDB"
    mysql_port = 6969
    mysql = MySQL(mysql_host, mysql_user, mysql_password, mysql_database, mysql_port)
    print("Conexión a MySQL establecida.")
    return mysql

# Muestra el menú
def show_menu():
    # Conectar a las bases de datos
    neo4j = connect_to_neo4j()
    mongodb = connect_to_mongodb()
    mysql = connect_to_mysql()

    # Menu
    menu = True
    while menu:
        print("\nMenu:")
        print("1. Personas y sus roles en una empresa concreta\n")
        print("2. Personas con el mismo rol en diferentes empresas.\n")
        print("3. Empresas comunes entre dos personas.\n")
        print("4. Personas y sus funciones en un equipo específico.\n")
        print("5. Muestra todos los equipos con el número de personas que los componen.\n")
        print("6. Muestra los equipos con el número total de proyectos a los que están asociados.\n")
        print("7. Obtener todas las skills en las que una persona tiene al menos un nivel específico de proficiency.\n")
        print("8. Encontrar todas las personas que tienen skill en al menos una skill en común con otra persona.\n")
        print("9. Encontrar el proyecto que tenga más personas en el equipo cuyos pokemons favoritos son de diferente tipo, mostrar todos los tipos distintos (Peticion API).\n")
        print("10. Dado una ubicación, obtén la lista de equipos que están ubicados allí junto con información de las personas que trabajan en ese equipo y los proyectos asociados.\n")
        print("99. Exit\n")
        
        choice = input("¿Qué desea hacer?\n")
        if choice == '1':
            empresa_name = input("Ingrese el nombre de la empresa: ")
            neo4j.consulta1(empresa_name)
        elif choice == '2':
            neo4j.consulta2()
        elif choice == '3':
            neo4j.consulta3()
        elif choice == '4':
            team_name = input("Ingrese el nombre del equipo: ")
            
            personas = neo4j.consulta7()
            # Crear un diccionario para mapear 'id' de personas a 'name'
            person_name_map = {persona['id']: persona['name'] for persona in personas}

            resultados = mongodb.consulta4(team_name)

            print(f"Resultados para el equipo {team_name}:")
            for resultado in resultados:

                # Reemplazar el person_id por el person_name usando el diccionario de personas
                if resultado['person_id'] in person_name_map:
                    resultado['person_name'] = person_name_map[resultado['person_id']]  # Asignar el nombre correspondiente
                
                print(resultado['persona_name'], resultado['rol'])
        elif choice == '5':
            print("a")
        elif choice == '6':
            print("a")
        elif choice == '7':
            proficiency = input("Ingrese el proficiency: ")
            personas = neo4j.consulta7()
            for persona in personas:
                persona_id = persona['id']
                persona_name = persona['name']
                skills = mysql.consulta7(persona_id,proficiency)
                if skills:
                    for skill in skills:
                        skill_name = skill[1]
                        proficiency = skill[2]
                        print(f"Persona: {persona_name}, Skill: {skill_name}, Proficiency: {proficiency}")
        elif choice == '8':
            print("a")
        elif choice == '9':
            print("a")
        elif choice == '10':
            print("a")           
        elif choice == '99':
            print("Cerrando conexiones...")
            mysql.close()
            neo4j.close()
            mongodb.close()
            print("Saliendo...")
            menu = False
        else:
            print("Opción invalida. Selecciona un numero del (1-10) o 99 para salir")

# Llamar a la función para mostrar el menú al ejecutar el script
if __name__ == "__main__":
    show_menu()
