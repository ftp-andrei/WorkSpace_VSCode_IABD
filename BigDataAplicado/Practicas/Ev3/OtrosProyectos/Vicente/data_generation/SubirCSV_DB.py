import psycopg2
import pandas as pd
import boto3

# Configuración de PostgreSQL
DB_CONFIG = {
    "host": "localhost",  # Servidor de la base de datos PostgreSQL
    "database": "retail_db",  # Nombre de la base de datos
    "user": "postgres",  # Usuario de la base de datos
    "password": "casa1234",  # Contraseña del usuario
    "port": 5432  # Puerto de conexión predeterminado de PostgreSQL
}

# Configuración de LocalStack (S3 local)
S3_CONFIG = {
    "endpoint_url": "http://localhost:4566",  # URL de LocalStack simulando S3
    "aws_access_key_id": "test",  # Clave de acceso ficticia para LocalStack
    "aws_secret_access_key": "test",  # Clave secreta ficticia para LocalStack
}

BUCKET_NAME = "bucket-1"  # Nombre del bucket en S3 (LocalStack)
CSV_FILE = "postgres_data.csv"  # Nombre del archivo CSV temporal
S3_FOLDER = "Postgres/"  # Subcarpeta dentro del bucket en S3

def export_db_to_csv():
    """Extrae datos de PostgreSQL y los guarda en un archivo CSV."""
    try:
        # Conectar a la base de datos PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        query = "SELECT * FROM Stores"  # Consulta SQL para obtener datos de la tabla Stores
        
        # Ejecutar la consulta y cargar los datos en un DataFrame de Pandas
        df = pd.read_sql(query, conn)
        
        # Guardar los datos en un archivo CSV sin incluir los índices
        df.to_csv(CSV_FILE, index=False)
        print(f"Datos exportados a {CSV_FILE}")
    except Exception as e:
        print(f"Error exportando datos: {e}")
    finally:
        # Cerrar la conexión a la base de datos
        if conn:
            conn.close()

def upload_to_s3():
    """Sube el archivo CSV a una subcarpeta en un bucket de S3 en LocalStack."""
    try:
        # Crear un cliente de S3 usando las credenciales de LocalStack
        s3_client = boto3.client("s3", **S3_CONFIG)

        # Verificar si el bucket ya existe en LocalStack
        existing_buckets = [b["Name"] for b in s3_client.list_buckets()["Buckets"]]
        if BUCKET_NAME not in existing_buckets:
            # Crear el bucket si no existe
            s3_client.create_bucket(Bucket=BUCKET_NAME)

        # Subir el archivo CSV al bucket dentro de la subcarpeta "Postgres/"
        s3_client.upload_file(CSV_FILE, BUCKET_NAME, f"{S3_FOLDER}{CSV_FILE}")
        print(f"Archivo {CSV_FILE} subido a {BUCKET_NAME}/{S3_FOLDER}")
    except Exception as e:
        print(f"Error subiendo a S3: {e}")

if __name__ == "__main__":
    # Ejecutar la exportación de la base de datos a CSV
    export_db_to_csv()
    
    # Subir el archivo CSV generado a S3 (LocalStack)
    upload_to_s3()
