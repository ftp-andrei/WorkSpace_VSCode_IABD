# docker run --name MySQLContainer -v VolumenMySQLContainer:/var/lib/mysql -p 4000:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql
# docker run --name MongoContainer -e MONGO_INITDB_ROOT_USERNAME=MarcosDB -e MONGO_INITDB_ROOT_PASSWORD=secreta -p 6969:27017 -v VolumenMongoContainer:/data/db -d mongo
# docker run  --name Neo4JContainer  --publish=7000:7474 --publish=8000:7687 --env NEO4J_AUTH=neo4j/MySecretPassword --volume VolumenNeo4JContainer:/data -d neo4j

from Comandos.CRUDNeo4J import Neo4jCRUD
from Comandos.CRUDMongo import MongoCRUD
from Comandos.CRUDMySQL import MySQLCRUD
from Comandos.UnificacionCRUD import Unificador
from Comandos.ConversorJSON_CSV import Conversor
from Comandos.Exportador import DBExporter
from colorama import Fore, Style

import os


in4j = Neo4jCRUD()
imdb= MongoCRUD()
imsql= MySQLCRUD()
unificador= Unificador()
conversor= Conversor() 
exportador= DBExporter()
respuesta='y'
estandatos='n'

# La ruta del directorio donde estan todos los datos falla dependiendo del ordenador

filepath= 'EjercicioBD\\AplicacionDataImport\\DataGeneration'
estandatos=input('Estan ya los datos metidos en las bases de datos? (y/n)\n')
while (estandatos=='n'):
    while (respuesta!='n'):  
        titulo = f"{Fore.CYAN}¿En qué lenguaje está la base de datos?{Style.RESET_ALL}"
        opciones = (f"{Fore.GREEN}1- Neo4j{Style.RESET_ALL}\n"
                    f"{Fore.YELLOW}2- MongoDB{Style.RESET_ALL}\n"
                    f"{Fore.BLUE}3- MySQL{Style.RESET_ALL}\n")
        lengbd = int(input(f"{titulo}\n{opciones}"))

        match (lengbd):
            case 1:
                tipoCreacion = int(input(f"{Fore.CYAN}¿Quieres crear un nodo o una relación?\n "
                                f"{Fore.GREEN}1- Nodo  {Style.RESET_ALL} \n"
                                f"{Fore.YELLOW}2- Relación  {Style.RESET_ALL} \n "
                                f"{Fore.RED}(Recuerda, primero crea los nodos que quieras relacionar y luego la relación) \n {Style.RESET_ALL}"))
                match(tipoCreacion):
                    case 1:
                        nodo= input(f"{Fore.LIGHTMAGENTA_EX} Cual es el nombre del nodo? \n {Style.RESET_ALL}")
                        filename=input(f"{Fore.LIGHTMAGENTA_EX}Cual es el nombre del archivo?\n {Style.RESET_ALL}")
                        
                        if (filename.endswith('.csv')):
                            nombre_sin_extension = os.path.splitext(filename)[0]
                            conversor.csv_to_json(f'{filepath}\\{filename}', f'{filepath}\\{nombre_sin_extension}.json')
                            filename=f'{nombre_sin_extension}.json'

                        in4j.crearNodos(nodo, f'{filepath}\\{filename}')

                    case 2:
                        nodo1= input(f"{Fore.LIGHTMAGENTA_EX}Cual es el nombre del nodo de origen? \n{Style.RESET_ALL}")
                        nodo2= input(f"{Fore.LIGHTMAGENTA_EX}Cual es el nombre del nodo de fin? \n{Style.RESET_ALL}")
                        idNodo1= input(f"{Fore.LIGHTMAGENTA_EX}Cual es el id del nodo de origen en su propia tabla? \n{Style.RESET_ALL}")
                        idNodo2= input(f"{Fore.LIGHTMAGENTA_EX}Cual es el id del nodo de fin en su propia tabla? \n{Style.RESET_ALL}")
                        filename=input(f"{Fore.LIGHTMAGENTA_EX}Cual es el nombre del csv en la que se relacionan? \n{Style.RESET_ALL}")
                        nombreRelacion=input(f"{Fore.LIGHTMAGENTA_EX}Cual es el nombre de la relacion? \n{Style.RESET_ALL}")
                        idTablaRelacion1=input(f"{Fore.LIGHTMAGENTA_EX}Cual es el id de origen de la tabla en la que se relacionan? \n{Style.RESET_ALL}")
                        idTablaRelacion2=input(f"{Fore.LIGHTMAGENTA_EX}Cual es el id de fin de la tabla en la que se relacionan? \n{Style.RESET_ALL}")

                        if (filename.endswith('.csv')):
                            nombre_sin_extension = os.path.splitext(filename)[0]
                            conversor.csv_to_json(f'{filepath}\\{filename}', f'{filepath}\\{nombre_sin_extension}.json')
                            filename=f'{nombre_sin_extension}.json'
                            
                        in4j.crearRelaciones(nodo1, idTablaRelacion1, nodo2, idTablaRelacion2, nombreRelacion, f'{filepath}\\{filename}', idNodo1, idNodo2)
                    case _: print()
            case 2: 
                collectionName= input(f'{Fore.LIGHTGREEN_EX}Como quieres llamar a la coleccion? \n{Style.RESET_ALL}')
                filename= input(f'{Fore.LIGHTGREEN_EX}Como se llama el archivo donde esta la coleccion? \n{Style.RESET_ALL}')
                id_tabla_original= input(f'{Fore.LIGHTGREEN_EX}Cual es su id? \n{Style.RESET_ALL}')
                if (filename.endswith('.csv')):
                            nombre_sin_extension = os.path.splitext(filename)[0]
                            conversor.csv_to_json(f'{filepath}\\{filename}', f'{filepath}\\{nombre_sin_extension}.json')
                            filename=f'{nombre_sin_extension}.json'
                
                imdb.crearColeccion(f'{filepath}\\{filename}', collectionName)

                relacionIncrustada= 'y'
                while(relacionIncrustada!='n'):
                    relacionIncrustada= input(f'{Fore.LIGHTGREEN_EX}¿Quieres generar una relacion incrustada? y/n \n {Style.RESET_ALL}')
                    if(relacionIncrustada!='y'):
                        break
                    tablaArray= input(F'{Fore.LIGHTGREEN_EX}De que archivo quieres que saquemos los datos? \n {Style.RESET_ALL}')
                    if (tablaArray.endswith('.csv')):
                            tablaArray_sin_extension = os.path.splitext(tablaArray)[0]
                            conversor.csv_to_json(f'{filepath}\\{tablaArray}', f'{filepath}\\{tablaArray_sin_extension}.json')
                            tablaArray=f'{tablaArray_sin_extension}.json'

                    atributoIdentificador= input(F'''{Fore.LIGHTGREEN_EX}Con que atributo puedo identificar de que tabla es? \n{Style.RESET_ALL}''')
                    nombreRIncrustada= input(F'{Fore.LIGHTGREEN_EX}Como quieres que se llame el atributo de relacion incrustada? \n {Style.RESET_ALL}')

                    imdb.nuevoDato(f'{filepath}\\{tablaArray}', nombreRIncrustada, atributoIdentificador, collectionName, id_tabla_original)
            case 3: 
                nombreTabla= input(F'{Fore.LIGHTRED_EX}Como quieres llamar a la tabla? \n {Style.RESET_ALL}')
                filename= input(F'{Fore.LIGHTRED_EX}Como se llama el archivo donde esta la tabla? \n {Style.RESET_ALL}')
                if (filename.endswith('.json')):
                            nombre_sin_extension = os.path.splitext(filename)[0]
                            conversor.convertir_json_a_csv(f'{filepath}\\{filename}', f'{filepath}\\{nombre_sin_extension}.csv')
                            filename=f'{nombre_sin_extension}.csv'
                
                imsql.create_table(f'{filepath}\\{filename}', nombreTabla)

                imsql.insert_data(f'{filepath}\\{filename}', nombreTabla)      
                
            case _: print()

        respuesta=input(F"{Fore.RED}¿Quieres continuar? y/n \n{Style.RESET_ALL}")
    estandatos=input('Estan ya los datos metidos en las bases de datos? (y/n)\n')

continuar='y'
while(continuar=='y'):
    menu = f"""
        {Fore.CYAN}Menú:
        {Fore.YELLOW}1. {Fore.GREEN}Personas y sus roles en una empresa concreta.
        {Fore.YELLOW}2. {Fore.GREEN}Personas con el mismo rol en diferentes empresas.
        {Fore.YELLOW}3. {Fore.GREEN}Empresas comunes entre dos personas.
        {Fore.YELLOW}4. {Fore.GREEN}Personas y sus funciones en un equipo específico.
        {Fore.YELLOW}5. {Fore.GREEN}Muestra todos los equipos con el número de personas que los componen.
        {Fore.YELLOW}6. {Fore.GREEN}Muestra los equipos con el número total de proyectos a los que están asociados.
        {Fore.YELLOW}7. {Fore.GREEN}Obtener todas las skills en las que una persona tiene al menos un nivel específico de proficiency.
        {Fore.YELLOW}8. {Fore.GREEN}Encontrar todas las personas que tienen skill en al menos una skill en común con otra persona (es decir, encontrar personas con skills similares).
        {Fore.YELLOW}9. {Fore.GREEN}Encontrar el proyecto que tenga más personas en el equipo cuyos pokemons favoritos son de diferente tipo, mostrar todos los tipos distintos.
        {Fore.YELLOW}10. {Fore.GREEN}Dado una ubicación, obtén la lista de equipos que están ubicados allí junto con información de las personas que trabajan en ese equipo y los proyectos asociados.{Style.RESET_ALL} \n"""

    consulta= int(input(menu))
    match(consulta):
        case 1:
            nombreEmpresa= input(f'{Fore.CYAN}De que empresa quieres buscar?{Style.RESET_ALL}\n')
            exportador.export_neo4j_result(unificador.Ejercicio1(nombreEmpresa), 'resultado1.json', 'json')
        case 2:
            exportador.export_neo4j_result(unificador.Ejercicio2(), 'resultado2.json', 'json')
        case 3:
            exportador.export_neo4j_result(unificador.Ejercicio3(), 'resultado3.json', 'json')
        case 4: 
            nombreEquipo= input(f'{Fore.CYAN}De que equipo quieres buscar?{Style.RESET_ALL}\n')
            print(unificador.Ejercicio4(nombreEquipo))
        case 5:
            exportador.export_mongo_result(unificador.Ejercicio5(), 'resultado5.json', 'json')
        case 6:
            print(unificador.Ejercicio6())
        case 7:
            nivelProeficiencia= input(f'{Fore.CYAN}Que nivel minimo quieres de proeficiencia?{Style.RESET_ALL}\n')
            resultado, columnas = unificador.Ejercicio7(nivelProeficiencia.lower())
            exportador.export_mysql_result(resultado, columnas, 'resultado7.json', 'json')
        case 8:
            print(unificador.Ejercicio8())
        case _:
            print()

    continuar=input('Quieres continuar? (y/n)\n')


