-- Cargamos archivo
pregunta_3 = LOAD '/data/raw/pregunta_3.csv' 
    USING PigStorage(',') 
    AS (vehiculo:CHARARRAY, numParadas:FLOAT, importeLinea:FLOAT, importeTodosVehiculos:FLOAT, conductores:FLATTEN);

conductor_mas_repetido = FOREACH (GROUP conductores ALL) GENERATE COUNT(conductores) AS total;

fecha_actual  =  FOREACH  conductor_mas_repetido  GENERATE  conductor, 
CURRENT_TIME() AS fecha;

-- Almacenar los datos limpios en HDFS
STORE fecha_actual INTO '/resultados/conductor_mas_repetido' USING PigStorage(',');
