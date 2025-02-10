-- Crear un script Pig para eliminar filas con más de 2 valores NULL

-- Cargar los datos procesados
data = LOAD '/home/datos_limpios'
    USING PigStorage(',')
    AS (nombre:CHARARRAY, profesion:CHARARRAY, estado:CHARARRAY, valor:CHARARRAY);

-- Contar cuántos valores NULL hay en cada fila
filtered_data = FILTER data BY 
    ((nombre == 'NULL' ? 1 : 0) + 
     (profesion == 'NULL' ? 1 : 0) + 
     (estado == 'NULL' ? 1 : 0) + 
     (valor == 'NULL' ? 1 : 0)) <= 2;

-- Guardar el resultado en HDFS
STORE filtered_data INTO '/home/datos_filtrados' USING PigStorage(',');