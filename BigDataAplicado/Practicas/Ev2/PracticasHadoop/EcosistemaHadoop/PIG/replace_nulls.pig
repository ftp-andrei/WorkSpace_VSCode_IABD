--  Crear el script Pig para reemplazar celdas vacías con "NULL"

-- Cargar el archivo CSV
data = LOAD '/home/datos.csv'
    USING PigStorage(',')
    AS (nombre:CHARARRAY, profesion:CHARARRAY, estado:CHARARRAY, valor:CHARARRAY);

-- Reemplazar valores vacíos por NULL
cleaned_data = FOREACH data GENERATE 
    (nombre is not null and nombre != '' ? nombre : 'NULL') AS nombre,
    (profesion is not null and profesion != '' ? profesion : 'NULL') AS profesion,
    (estado is not null and estado != '' ? estado : 'NULL') AS estado,
    (valor is not null and valor != '' ? valor : 'NULL') AS valor;

-- Almacenar los datos limpios en HDFS
STORE cleaned_data INTO '/home/datos_limpios' USING PigStorage(',');