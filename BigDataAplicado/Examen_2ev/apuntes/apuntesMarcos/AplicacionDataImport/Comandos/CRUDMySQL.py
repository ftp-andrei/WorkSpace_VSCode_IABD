# docker run --name MySQLContainer -v VolumenMySQLContainer:/var/lib/mysql -p 4000:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql
# docker run --name MongoContainer -e MONGO_INITDB_ROOT_USERNAME=MarcosDB -e MONGO_INITDB_ROOT_PASSWORD=secreta -p 6969:27017 -v VolumenMongoContainer:/data/db -d mongo
# docker run  --name Neo4JContainer  --publish=7000:7474 --publish=8000:7687 --env NEO4J_AUTH=neo4j/MySecretPassword --volume VolumenNeo4JContainer:/data -d neo4j


import mysql.connector 
import pandas as pd
from colorama import Style, Fore

class MySQLCRUD:
    def __init__(self):

        host='localhost'
        user='root'
        port='4000'
        password='root'
        database= 'DB_prueba'
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            port=port,
            password=password,
        )
        self.cursor = self.connection.cursor()

        

        self.create_database(database)

        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            port=port,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()


    def create_database(self, database):
        try:
            create_db_query = f"CREATE DATABASE IF NOT EXISTS {database}"
            self.cursor.execute(create_db_query)
            self.connection.commit()
            print(f"{Fore.GREEN}Base de datos '{database}' creada correctamente.{Style.RESET_ALL}")
        except mysql.connector.Error as err:
            print(f"{Fore.RED}Error al crear la base de datos: {err} {Style.RESET_ALL}")


    def create_table(self, csv_path, nombreTabla):
        df = pd.read_csv(csv_path)
        columns = df.columns

        # Empezamos a construir la consulta de creación de la tabla
        create_table_query = f"CREATE TABLE IF NOT EXISTS {nombreTabla} ("
        compId= input("Tiene id la tabla? y/n \n")

        if compId=='y':
            create_table_query += f"id INT AUTO_INCREMENT PRIMARY KEY, "
        # Lista para almacenar las claves foráneas que vamos a agregar al final
        foreign_keys = []
        
        # Recorrer las demás columnas
        for col in columns:  # Asegurarnos de no añadir 'id' de nuevo
                print(f"Para la columna '{col}': \n")
                print(f"¿De qué tipo va a ser? \n")
                print("Ejemplos de tipos: INT, FLOAT, VARCHAR(255), DATE \n")
                tipoVar = input(f"Tipo de variable para {col}: \n")
                print('\n')
                print(f"¿Qué restricciones quieres agregar? (Deja en blanco si no deseas ninguna) \n")
                print("Ejemplos de restricciones: PRIMARY KEY, UNIQUE, NOT NULL \n")
                constraints = input(f"Restricciones para {col}: \n")
                print('\n')

                # Manejo de clave foránea
                foreign_key = input(f"¿La columna '{col}' será una clave foránea? (y/n): \n (Recuerda que tiene que estar creada la tabla a la que hace referencia de antes) \n").lower()

                if foreign_key == 'y':
                    referencia_tabla = input(f"¿A qué tabla hace referencia la columna '{col}'? \n")
                    print('\n')
                    referencia_columna = input(f"¿A qué columna de la tabla '{referencia_tabla}' hace referencia? \n")
                    print('\n')
                    foreign_keys.append(f"CONSTRAINT fk_{col} FOREIGN KEY ({col}) REFERENCES {referencia_tabla}({referencia_columna})")
                    
                    # Si la restricción ON DELETE es proporcionada, la agregamos correctamente
                    on_delete = input(f"¿Qué acción quieres para ON DELETE en la columna '{col}'? (Ejemplo: CASCADE, SET NULL) \n")
                    if on_delete:
                        foreign_keys[-1] += f" ON DELETE {on_delete}"

                # Si el usuario proporciona restricciones, las agregamos a la columna
                if constraints:
                    create_table_query += f"{col} {tipoVar} {constraints}, "
                else:
                    create_table_query += f"{col} {tipoVar}, "

        # Finalizamos la consulta de creación de la tabla (eliminamos la última coma)
        create_table_query = create_table_query.rstrip(", ")

        # Agregar las claves foráneas al final de la consulta
        if foreign_keys:
            create_table_query += ", " + ", ".join(foreign_keys)

        # Cerrar la definición de la tabla
        create_table_query += ")"

        # Imprimimos la consulta de creación para depuración
        print(f"Consulta de creación de la tabla: {create_table_query}")

        # Ejecutamos la consulta para crear la tabla
        self.cursor.execute(create_table_query)
        self.connection.commit()


    def insert_data(self, csv_path, nombreTabla):
        df = pd.read_csv(csv_path)
        columns = df.columns
        placeholders = ", ".join(["%s"] * len(columns))
        insert_query = f"INSERT INTO {nombreTabla} ({', '.join(columns)}) VALUES ({placeholders})"
        
        for _, row in df.iterrows():
            self.cursor.execute(insert_query, tuple(row))
        
        self.connection.commit()

    def DesdeProeficiencia(self, nivelProeficiencia):
        query= "SELECT DISTINCT h.* FROM tiene_habilidad t JOIN habilidades h ON t.skill_id=h.id WHERE LOWER(t.proficiency) LIKE %s"
        self.cursor.execute(query, (f"%{nivelProeficiencia.lower()}%",))
        result = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        return result, column_names
    
    def skillsComunes(self):
        query= """SELECT t.person_id
                FROM tiene_habilidad t
                JOIN (
                    SELECT skill_id
                    FROM tiene_habilidad
                    GROUP BY skill_id
                    HAVING COUNT(skill_id) > 1
                ) AS habilidades_comunes
                ON t.skill_id = habilidades_comunes.skill_id;"""
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result