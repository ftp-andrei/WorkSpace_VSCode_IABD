-- 5. Eliminar duplicados
-- Elimina las filas duplicadas de un archivo de datos:

-- Cargar los datos
data = LOAD '/home/duplicados' 
    USING PigStorage(',') 
    AS (col1:CHARARRAY, col2:CHARARRAY, col3:CHARARRAY);

-- Eliminar duplicados
distinct_data = DISTINCT data;

-- Guardar el resultado
STORE distinct_data INTO '/home/sin_duplicados' USING PigStorage(',');
