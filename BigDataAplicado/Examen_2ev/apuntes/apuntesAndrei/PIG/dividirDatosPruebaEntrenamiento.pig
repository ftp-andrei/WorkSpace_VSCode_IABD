-- 10. Dividir los datos en dos conjuntos (entrenamiento y prueba)
-- Divide un conjunto de datos en dos subconjuntos: 70% para entrenamiento y 30% para prueba:


-- Cargar los datos
data = LOAD '/home/datos' 
    USING PigStorage(',') 
    AS (id:CHARARRAY, atributo1:CHARARRAY, atributo2:CHARARRAY);

-- Asignar un número aleatorio a cada fila
data_with_random = FOREACH data GENERATE 
    id, 
    atributo1, 
    atributo2, 
    RANDOM() AS random_value;

-- Dividir en 70% entrenamiento y 30% prueba
train_data = FILTER data_with_random BY random_value <= 0.7;
test_data = FILTER data_with_random BY random_value > 0.7;

-- Guardar los resultados
STORE train_data INTO '/home/train_data' USING PigStorage(',');
STORE test_data INTO '/home/test_data' USING PigStorage(',');
