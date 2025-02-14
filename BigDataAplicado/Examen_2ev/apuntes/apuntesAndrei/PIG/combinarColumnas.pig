-- 11. Combinar dos conjuntos de datos
-- Une dos conjuntos de datos basados en una columna común (similar a un JOIN en SQL):

-- Cargar los datos
data1 = LOAD '/home/datos1' 
    USING PigStorage(',') 
    AS (id:CHARARRAY, nombre:CHARARRAY, edad:INT);

data2 = LOAD '/home/datos2' 
    USING PigStorage(',') 
    AS (id:CHARARRAY, profesion:CHARARRAY, salario:DOUBLE);

-- Realizar un JOIN basado en la columna id
joined_data = JOIN data1 BY id, data2 BY id;

-- Guardar el resultado
STORE joined_data INTO '/home/datos_combinados' USING PigStorage(',');
