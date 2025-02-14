-- Cargar datos desde un archivo CSV y visualizar
productos = LOAD '/path/to/productos.csv' USING PigStorage(',') AS (id:int, nombre:chararray, categoria:chararray, precio:float);
DUMP productos;

-- Filtrar productos con precio mayor a 50
productos = LOAD '/path/to/productos.csv' USING PigStorage(',') AS (id:int, nombre:chararray, categoria:chararray, precio:float);
productos_filtrados = FILTER productos BY precio > 50;
DUMP productos_filtrados;

-- Seleccionar las columnas nombre y precio
productos = LOAD '/path/to/productos.csv' USING PigStorage(',') AS (id:int, nombre:chararray, categoria:chararray, precio:float, stock:int);
seleccion = FOREACH productos GENERATE nombre, precio;
DUMP seleccion;

-- Eliminar duplicados en las transacciones
transacciones = LOAD '/path/to/transacciones.csv' USING PigStorage(',') AS (id:int, usuario:chararray, producto:int, cantidad:int, total:float);
transacciones_distintas = DISTINCT transacciones;
DUMP transacciones_distintas;

-- Ordenar usuarios por edad
usuarios = LOAD '/path/to/usuarios.csv' USING PigStorage(',') AS (id:int, nombre:chararray, edad:int, ciudad:chararray);
usuarios_ordenados = ORDER usuarios BY edad ASC;
DUMP usuarios_ordenados;

-- Contar el total de productos | Contar filas en un dataset
productos = LOAD '/path/to/productos.csv' USING PigStorage(',') AS (id:int, nombre:chararray, categoria:chararray, precio:float);
total_productos = FOREACH (GROUP productos ALL) GENERATE COUNT(productos);
DUMP total_productos;

-- Contar productos por categoría | Agrupar por categoría y contar productos
productos = LOAD '/path/to/productos.csv' USING PigStorage(',') AS (id:int, nombre:chararray, categoria:chararray, precio:float);
productos_por_categoria = GROUP productos BY categoria;
conteo = FOREACH productos_por_categoria GENERATE group AS categoria, COUNT(productos) AS total;
DUMP conteo;

-- Promedio de precios por categoría | Calcular promedio de precios por categoría
productos = LOAD '/path/to/productos.csv' USING PigStorage(',') AS (id:int, nombre:chararray, categoria:chararray, precio:float);
productos_por_categoria = GROUP productos BY categoria;
promedio_precio = FOREACH productos_por_categoria GENERATE group AS categoria, AVG(productos.precio) AS promedio_precio;
DUMP promedio_precio;

-- Producto con el precio más alto/caro
productos = LOAD '/path/to/productos.csv' USING PigStorage(',') AS (id:int, nombre:chararray, categoria:chararray, precio:float);
max_precio = FOREACH (GROUP productos ALL) GENERATE MAX(productos.precio) AS precio_maximo;
DUMP max_precio;

-- Contar cuántas transacciones tiene cada usuario
transacciones = LOAD '/path/to/transacciones.csv' USING PigStorage(',') AS (id:int, usuario:chararray, producto:int, cantidad:int, total:float);
transacciones_por_usuario = GROUP transacciones BY usuario;
conteo = FOREACH transacciones_por_usuario GENERATE group AS usuario, COUNT(transacciones) AS total_transacciones;
DUMP conteo;

-- Calcular las ventas totales de cada producto
transacciones = LOAD '/path/to/transacciones.csv' USING PigStorage(',') AS (id:int, usuario:chararray, producto:int, cantidad:int, total:float);
ventas_por_producto = GROUP transacciones BY producto;
suma_ventas = FOREACH ventas_por_producto GENERATE group AS producto, SUM(transacciones.total) AS total_ventas;
DUMP suma_ventas;

-- Eliminar registros donde los campos sean NULL
productos = LOAD '/path/to/productos.csv' USING PigStorage(',') AS (id:int, nombre:chararray, categoria:chararray, precio:float);
productos_validos = FILTER productos BY nombre IS NOT NULL AND precio IS NOT NULL;
DUMP productos_validos;

-- Calcular un nuevo campo con descuento aplicado
productos = LOAD '/path/to/productos.csv' USING PigStorage(',') AS (id:int, nombre:chararray, categoria:chararray, precio:float);
productos_con_descuento = FOREACH productos GENERATE id, nombre, categoria, precio, precio * 0.9 AS precio_descuento;
DUMP productos_con_descuento;

-- Dividir los productos en caros y baratos
productos = LOAD '/path/to/productos.csv' USING PigStorage(',') AS (id:int, nombre:chararray, categoria:chararray, precio:float);
productos_caros = FILTER productos BY precio > 100;
productos_baratos = FILTER productos BY precio <= 100;
DUMP productos_caros;
DUMP productos_baratos;

-- Hacer un JOIN entre usuarios y transacciones
usuarios = LOAD '/path/to/usuarios.csv' USING PigStorage(',') AS (id:int, nombre:chararray, edad:int);
transacciones = LOAD '/path/to/transacciones.csv' USING PigStorage(',') AS (id:int, usuario_id:int, producto:int, total:float);
usuarios_transacciones = JOIN usuarios BY id, transacciones BY usuario_id;
DUMP usuarios_transacciones;

-- Sumar, contar y calcular promedio por categoría
productos = LOAD '/path/to/productos.csv' USING PigStorage(',') AS (id:int, nombre:chararray, categoria:chararray, precio:float);
productos_por_categoria = GROUP productos BY categoria;
metricas = FOREACH productos_por_categoria GENERATE group AS categoria, COUNT(productos) AS total_productos, SUM(productos.precio) AS suma_precios, AVG(productos.precio) AS promedio_precio;
DUMP metricas;

-- Guardar los resultados de productos caros en HDFS
productos_caros = FILTER productos BY precio > 100;
STORE productos_caros INTO '/output/productos_caros' USING PigStorage(',');

-- Mostrar solo las primeras 10 filas de productos | Limitar el número de registros
productos = LOAD '/path/to/productos.csv' USING PigStorage(',') AS (id:int, nombre:chararray, categoria:chararray, precio:float);
primeros_productos = LIMIT productos 10;
DUMP primeros_productos;

-- Unir datos de diferentes regiones | Unir múltiples datasets
data1 = LOAD '/path/to/region1.csv' USING PigStorage(',') AS (id:int, valor:float);
data2 = LOAD '/path/to/region2.csv' USING PigStorage(',') AS (id:int, valor:float);
union_data = UNION data1, data2;
DUMP union_data;

-- Contar palabras en un archivo de texto
lines = LOAD '/path/to/textfile.txt' USING TextLoader() AS (line:chararray);
words = FOREACH lines GENERATE FLATTEN(TOKENIZE(line)) AS word;
grouped_words = GROUP words BY word;
word_count = FOREACH grouped_words GENERATE group AS word, COUNT(words) AS count;
DUMP word_count;
