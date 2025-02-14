-- 2. Contar ocurrencias de un valor en una columna
-- Cuenta cuántos productos pertenecen a la categoría Electrónica:

-- Cargar los datos
data = LOAD '/home/productos' 
    USING PigStorage(',') 
    AS (producto:CHARARRAY, categoria:CHARARRAY, precio:DOUBLE);

-- Filtrar productos de la categoría Electrónica
electronics = FILTER data BY categoria == 'Electrónica';

-- Contar productos
count_electronics = FOREACH (GROUP electronics ALL) GENERATE COUNT(electronics) AS total;

-- Guardar el resultado
STORE count_electronics INTO '/home/total_electronica' USING PigStorage(',');
