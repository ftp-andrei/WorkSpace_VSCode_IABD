-- Cargamos archivo
pregunta_1 = LOAD '/data/raw/pregunta_1.csv' 
    USING PigStorage(',') 
    AS (linea:CHARARRAY, hora_inicio:CHARARRAY, hora_fin:CHARARRAY, conductores:FLATTEN, vehiculos:FLATTEN, precio:DOUBLE, descuento:FLOAT);
-- Eliminar registros donde los campos sean NULL
clean_pregunta_1 = FILTER pregunta_1 BY linea IS NOT NULL AND hora_inicio IS NOT NULL AND hora_fin IS NOT NULL AND conductores IS NOT NULL vehiculos IS NOT NULL AND precio IS NOT NULL AND descuento IS NOT NULL;

-- Almacenar los datos limpios en HDFS
STORE clean_pregunta_1 INTO '/data/raw/pregunta_1_limpio' USING PigStorage(',');

-- Cargamos archivo
pregunta_2 = LOAD '/data/raw/pregunta_2.csv' 
    USING PigStorage(',') 
    AS (vehiculos:CHARARRAY, latitud:FLOAT, longitud:FLOAT, timestamp:CHARARRAY, lineas:FLATTEN, paradas:FLATTEN);
-- Eliminar registros donde los campos sean NULL
clean_pregunta_2 = FILTER pregunta_2 BY vehiculos IS NOT NULL AND latitud IS NOT NULL AND longitud IS NOT NULL AND timestamp IS NOT NULL lineas IS NOT NULL AND paradas IS NOT NULL;

-- Almacenar los datos limpios en HDFS
STORE clean_pregunta_2 INTO '/data/raw/pregunta_2_limpio' USING PigStorage(',');


-- Cargamos archivo
pregunta_3 = LOAD '/data/raw/pregunta_3.csv' 
    USING PigStorage(',') 
    AS (vehiculo:CHARARRAY, numParadas:FLOAT, importeLinea:FLOAT, importeTodosVehiculos:FLOAT, conductores:FLATTEN);
-- Eliminar registros donde los campos sean NULL
clean_pregunta_3 = FILTER pregunta_3 BY vehiculo IS NOT NULL AND numParadas IS NOT NULL AND importeLinea IS NOT NULL AND importeTodosVehiculos IS NOT NULL conductores IS NOT NULL;

-- Almacenar los datos limpios en HDFS
STORE clean_pregunta_3 INTO '/data/raw/pregunta_3_limpio' USING PigStorage(',');

