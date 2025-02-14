-- 7. Encontrar el valor máximo y mínimo por grupo
-- Calcula los valores máximo y mínimo de la columna valor agrupados por categoria.

-- Cargar los datos
data = LOAD '/home/datos' 
    USING PigStorage(',') 
    AS (id:CHARARRAY, categoria:CHARARRAY, valor:DOUBLE);

-- Agrupar por categoría
grouped_data = GROUP data BY categoria;

-- Calcular valor máximo y mínimo
min_max_values = FOREACH grouped_data GENERATE 
    group AS categoria, 
    MIN(data.valor) AS valor_minimo, 
    MAX(data.valor) AS valor_maximo;

-- Guardar el resultado
STORE min_max_values INTO '/home/valores_min_max' USING PigStorage(',');
