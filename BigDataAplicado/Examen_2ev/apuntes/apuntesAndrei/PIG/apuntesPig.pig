-- 1. Cargar datos desde HDFS
-- Carga un archivo CSV desde HDFS y define los campos con sus tipos
data = LOAD '/path/to/data' USING PigStorage(',') AS (field1:chararray, field2:int, field3:float);
DUMP data;

-- 2. Filtrar filas según una condición
-- Filtra los datos donde field2 sea mayor que 100
filtered_data = FILTER data BY field2 > 100;
DUMP filtered_data;

-- 3. Seleccionar columnas específicas
-- Extrae las columnas field1 y field3
selected_columns = FOREACH data GENERATE field1, field3;
DUMP selected_columns;

-- 4. Eliminar duplicados
-- Elimina filas duplicadas en la relación
distinct_data = DISTINCT data;
DUMP distinct_data;

-- 5. Ordenar los datos
-- Ordena los datos en orden descendente por field2
sorted_data = ORDER data BY field2 DESC;
DUMP sorted_data;

-- 6. Contar el número total de filas
-- Cuenta el número total de registros en la relación
row_count = FOREACH (GROUP data ALL) GENERATE COUNT(data);
DUMP row_count;

-- 7. Calcular promedios
-- Calcula el promedio de field3
grouped_data = GROUP data ALL;
avg_value = FOREACH grouped_data GENERATE AVG(data.field3);
DUMP avg_value;

-- 8. Suma total de una columna
-- Calcula la suma de field3
grouped_data = GROUP data ALL;
sum_value = FOREACH grouped_data GENERATE SUM(data.field3);
DUMP sum_value;

-- 9. Encontrar el valor máximo
-- Encuentra el valor máximo de field3
grouped_data = GROUP data ALL;
max_value = FOREACH grouped_data GENERATE MAX(data.field3);
DUMP max_value;

-- 10. Encontrar el valor mínimo
-- Encuentra el valor mínimo de field3
grouped_data = GROUP data ALL;
min_value = FOREACH grouped_data GENERATE MIN(data.field3);
DUMP min_value;

-- 11. Agrupar por una columna
-- Agrupa los datos por field1
grouped_by_field1 = GROUP data BY field1;
DUMP grouped_by_field1;

-- 12. Contar filas por grupo
-- Cuenta cuántos registros hay por cada valor de field1
grouped_data = GROUP data BY field1;
count_per_group = FOREACH grouped_data GENERATE group, COUNT(data);
DUMP count_per_group;

-- 13. Join entre dos datasets
-- Realiza una unión entre dos relaciones por la columna id
data1 = LOAD '/path/to/data1' USING PigStorage(',') AS (id:int, name:chararray);
data2 = LOAD '/path/to/data2' USING PigStorage(',') AS (id:int, salary:float);
joined_data = JOIN data1 BY id, data2 BY id;
DUMP joined_data;

-- 14. Cálculo de valores derivados
-- Crea una nueva columna duplicando los valores de field2
derived_data = FOREACH data GENERATE field1, field2 * 2 AS doubled_field2;
DUMP derived_data;

-- 15. Filtrar datos nulos
-- Elimina las filas donde field1 o field3 sean NULL
non_null_data = FILTER data BY field1 IS NOT NULL AND field3 IS NOT NULL;
DUMP non_null_data;

-- 16. Dividir datos en subconjuntos
-- Divide los datos en dos subconjuntos según el valor de field3
high_salary_data = FILTER data BY field3 > 5000;
low_salary_data = FILTER data BY field3 <= 5000;
DUMP high_salary_data;
DUMP low_salary_data;

-- 17. Unir datasets (Union)
-- Une dos relaciones en una sola
data1 = LOAD '/path/to/data1' USING PigStorage(',');
data2 = LOAD '/path/to/data2' USING PigStorage(',');
union_data = UNION data1, data2;
DUMP union_data;

-- 18. Agrupar datos y calcular múltiples valores (SUM, AVG, COUNT)
-- Calcula varias métricas agregadas por cada valor único de field1
grouped_data = GROUP data BY field1;
stats = FOREACH grouped_data GENERATE group, SUM(data.field3), AVG(data.field3), COUNT(data);
DUMP stats;

-- 19. Escribir datos procesados en HDFS
-- Guarda los resultados en un archivo en HDFS
STORE data INTO '/path/to/output' USING PigStorage(',');

-- 20. Cargar datos JSON
-- Carga un archivo JSON con la definición de sus campos
data = LOAD '/path/to/json_data' USING JsonLoader('field1:chararray, field2:int, field3:float');
DUMP data;
