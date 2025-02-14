-- 1. Filtrar filas con valores específicos en una columna
-- Elimina todas las filas donde la columna estado tenga el valor INACTIVO:

-- Cargar los datos
data = LOAD '/home/empleados' 
    USING PigStorage(',') 
    AS (nombre:CHARARRAY, profesion:CHARARRAY, estado:CHARARRAY, valor:CHARARRAY);

-- Filtrar filas donde el estado no sea INACTIVO
filtered_data = FILTER data BY estado != 'INACTIVO';

-- Guardar el resultado
STORE filtered_data INTO '/home/empleados_activos' USING PigStorage(',');
