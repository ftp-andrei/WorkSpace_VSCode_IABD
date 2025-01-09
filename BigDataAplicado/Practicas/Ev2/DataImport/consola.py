
# from mainNeo4j import Neo4jCRUD
uri = "bolt://localhost:7687"  
user = "neo4j"
password = "password"
# neo4j = Neo4jCRUD(uri, user, password)
        
while True:
    print("\nMenu:")
    print("1. Personas y sus roles en una empresa concreta")
    print("2. Personas con el mismo rol en diferentes empresas.")
    print("3. Empresas comunes entre dos personas.")
    print("4. Personas y sus funciones en un equipo específico.")
    print("5. Muestra todos los equipos con el número de personas que los componen.")
    print("6. Muestra los equipos con el número total de proyectos a los que están asociados.")
    print("7. Muestra los equipos con el número total de proyectos a los que están asociados.")
    print("8. Muestra los equipos con el número total de proyectos a los que están asociados.")
    print("9. Muestra los equipos con el número total de proyectos a los que están asociados.")
    choice = input("¿Qué desea hacer?")
    
    if choice == '1':
        print("a")
    elif choice == '2':
        print("a")
    elif choice == '3':
        print("a")
    elif choice == '4':
        print("a")
    elif choice == '5':
        print("a")
    elif choice == '6':
        print("a")
    else:
        print("Invalid choice. Please select a valid option.")
