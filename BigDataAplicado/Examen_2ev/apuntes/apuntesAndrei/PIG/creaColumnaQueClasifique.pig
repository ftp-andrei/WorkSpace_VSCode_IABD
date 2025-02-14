-- 9. Crear una nueva columna basada en condiciones
-- Añade una columna llamada categoria_valor que clasifique los valores de la columna valor como ALTO, MEDIO o BAJO:

-- Cargar los datos
data = LOAD '/home/ventas' 
    USING PigStorage(',') 
    AS (id:CHARARRAY, cliente:CHARARRAY, valor:DOUBLE);

-- Clasificar los valores
classified_data = FOREACH data GENERATE
    id,
    cliente,
    valor,
    (valor > 1000 ? 'ALTO' : (valor > 500 ? 'MEDIO' : 'BAJO')) AS categoria_valor;

-- Guardar el resultado
STORE classified_data INTO '/home/ventas_clasificadas' USING PigStorage(',');
