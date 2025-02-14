-- 3. Ordenar datos por una columna
-- Ordena los datos por la columna valor en orden descendente:

-- Cargar los datos
data = LOAD '/home/ventas' 
    USING PigStorage(',') 
    AS (id:CHARARRAY, cliente:CHARARRAY, valor:DOUBLE, fecha:CHARARRAY);

-- Ordenar los datos por la columna valor en orden descendente
sorted_data = ORDER data BY valor DESC;

-- Guardar el resultado
STORE sorted_data INTO '/home/ventas_ordenadas' USING PigStorage(',');
