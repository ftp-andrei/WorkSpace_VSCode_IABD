from claseNeo4j import Neo4J
from claseMongoDB import MongoDB
from claseMySQL import MySQL

# Muestra el menu
def show_menu():
    menu= True
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
        print("9. Encontrar el proyecto que tenga más personas en el equipo cuyos pokemons favoritos son de diferente tipo, mostrar todo los tipos distintos (Peticion API).\n")
        print("10. Dado una ubicación, obtén la lista de equipos que están ubicados allí junto con información de las personas que trabajan en ese equipo y los proyectos asociados.\n")
        print("99. Exit")
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
        elif choice == '7':
            print("a")
        elif choice == '8':
            print("a")
        elif choice == '9':
            print("a")
        elif choice == '10':
            print("a")           
        elif choice == '99':
            print("Saliendo...")
            menu=False
        else:
            print("Invalid choice. Please select a valid option.")

# Llamar a la función para mostrar el menú al ejecutar el script
if __name__ == "__main__":
    show_menu()
