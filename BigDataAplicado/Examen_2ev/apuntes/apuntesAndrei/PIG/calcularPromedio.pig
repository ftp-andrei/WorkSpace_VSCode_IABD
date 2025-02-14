-- 4. Agrupar y calcular promedios
-- Agrupa los datos por la columna estado y calcula el promedio de la columna valor para cada grupo:

-- Cargar los datos
data = LOAD '/home/estudiantes' 
    USING PigStorage(',') 
    AS (nombre:CHARARRAY, estado:CHARARRAY, valor:DOUBLE);

-- Agrupar por estado
grouped_data = GROUP data BY estado;

-- Calcular el promedio de la columna valor
average_value = FOREACH grouped_data GENERATE group AS estado, AVG(data.valor) AS promedio;

-- Guardar el resultado
STORE average_value INTO '/home/promedios_estados' USING PigStorage(',');
