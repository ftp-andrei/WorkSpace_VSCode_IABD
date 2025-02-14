-- 8. Calcular porcentaje de valores nulos en cada columna
-- Determina el porcentaje de valores NULL en cada columna de un archivo:

-- Cargar los datos
data = LOAD '/home/datos' 
    USING PigStorage(',') 
    AS (col1:CHARARRAY, col2:CHARARRAY, col3:CHARARRAY);

-- Calcular el total de filas
total_rows = FOREACH (GROUP data ALL) GENERATE COUNT(data) AS total;

-- Contar los valores NULL por columna
null_counts = FOREACH (GROUP data ALL) GENERATE
    (COUNT(data) - COUNT(data.col1)) AS nulls_col1,
    (COUNT(data) - COUNT(data.col2)) AS nulls_col2,
    (COUNT(data) - COUNT(data.col3)) AS nulls_col3;

-- Calcular el porcentaje de NULLs
percent_nulls = FOREACH (CROSS null_counts, total_rows) GENERATE
    (nulls_col1 * 100 / total.total) AS percent_null_col1,
    (nulls_col2 * 100 / total.total) AS percent_null_col2,
    (nulls_col3 * 100 / total.total) AS percent_null_col3;

-- Guardar el resultado
STORE percent_nulls INTO '/home/porcentaje_nulos' USING PigStorage(',');
