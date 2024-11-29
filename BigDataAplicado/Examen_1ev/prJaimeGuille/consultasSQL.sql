+---------------------------+
| Tables_in_EmpresaFicticia |
+---------------------------+
| Departamentos             |
| Empleados                 |
| Empleados_Proyectos       |
| Proyectos                 |
+---------------------------+


Obtener el salario promedio de los empleados por departamento.
SELECT d.nombre, AVG(e.salario)
FROM Empleados e JOIN Departamentos d ON e.departamento_id = d.departamento_id
GROUP BY d.nombre;


Listar los proyectos con más de 100 horas trabajadas en total.
SELECT p.nombre AS proyecto, SUM(ep.horas_trabajadas) AS total_horas
FROM Proyectos p
JOIN Empleados_Proyectos ep ON p.proyecto_id = ep.proyecto_id
GROUP BY p.nombre
HAVING total_horas > 100;

Obtener los empleados que han trabajado en más de un proyecto.
SELECT e.nombre, e.apellido, COUNT(ep.proyecto_id) AS numero_proyectos
FROM Empleados e
JOIN Empleados_Proyectos ep ON e.empleado_id = ep.empleado_id
GROUP BY e.empleado_id
HAVING numero_proyectos > 1;

Encontrar el proyecto con el presupuesto más alto.
SELECT nombre, presupuesto 
FROM Proyectos 
ORDER BY presupuesto DESC 
LIMIT 1;

Listar empleados que trabajan en el proyecto 'Proyecto Alpha'.
SELECT e.nombre, e.apellido
FROM Empleados e
JOIN Empleados_Proyectos ep ON e.empleado_id = ep.empleado_id
JOIN Proyectos p ON ep.proyecto_id = p.proyecto_id
WHERE p.nombre = 'Proyecto Alpha';

Calcular el total de horas trabajadas por cada empleado.
SELECT e.nombre, e.apellido, SUM(ep.horas_trabajadas) AS total_horas
FROM Empleados e
JOIN Empleados_Proyectos ep ON e.empleado_id = ep.empleado_id
GROUP BY e.empleado_id;



------------------------------
CREATE DATABASE PracticaSQL;
USE PracticaSQL;

CREATE TABLE Clientes (
    cliente_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    email VARCHAR(100),
    fecha_registro DATE
);

CREATE TABLE Productos (
    producto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_producto VARCHAR(100),
    precio DECIMAL(10,2),
    stock INT
);

CREATE TABLE Proveedores (
    proveedor_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_proveedor VARCHAR(100),
    telefono VARCHAR(20)
);

CREATE TABLE Compras (
    compra_id INT AUTO_INCREMENT PRIMARY KEY,
    proveedor_id INT,
    fecha_compra DATE,
    total_compra DECIMAL(10,2),
    FOREIGN KEY (proveedor_id) REFERENCES Proveedores(proveedor_id)
);

CREATE TABLE Detalle_Compras (
    detalle_compra_id INT AUTO_INCREMENT PRIMARY KEY,
    compra_id INT,
    producto_id INT,
    cantidad INT,
    precio_compra DECIMAL(10,2),
    FOREIGN KEY (compra_id) REFERENCES Compras(compra_id),
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
);

CREATE TABLE Pedidos (
    pedido_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    fecha_pedido DATE,
    total DECIMAL(10,2),
    FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id)
);

CREATE TABLE Detalle_Pedidos (
    detalle_id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    producto_id INT,
    cantidad INT,
    precio_unitario DECIMAL(10,2),
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(pedido_id),
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
);

INSERT INTO Clientes (nombre, apellido, email, fecha_registro) VALUES
('Juan', 'Pérez', 'juan.perez@example.com', '2023-01-15'),
('María', 'García', 'maria.garcia@example.com', '2023-02-20'),
('Luis', 'López', 'luis.lopez@example.com', '2023-03-05'),
('Ana', 'Martínez', 'ana.martinez@example.com', '2023-04-10'),
('Pedro', 'Sánchez', 'pedro.sanchez@example.com', '2023-05-25');

INSERT INTO Productos (nombre_producto, precio, stock) VALUES
('Laptop', 1200.00, 50),
('Mouse', 25.00, 300),
('Teclado', 45.00, 150),
('Monitor', 250.00, 80),
('Impresora', 150.00, 40);

INSERT INTO Proveedores (nombre_proveedor, telefono) VALUES
('Tech Supplies Inc.', '123-456-7890'),
('Hardware Pro', '987-654-3210'),
('Office World', '456-789-1230');

INSERT INTO Compras (proveedor_id, fecha_compra, total_compra) VALUES
(1, '2023-06-10', 3000.00),
(2, '2023-06-15', 1500.00),
(3, '2023-07-01', 500.00);

INSERT INTO Detalle_Compras (compra_id, producto_id, cantidad, precio_compra) VALUES
(1, 1, 10, 1100.00),
(1, 2, 100, 20.00),
(2, 3, 50, 40.00),
(2, 4, 20, 200.00),
(3, 5, 5, 140.00);

INSERT INTO Pedidos (cliente_id, fecha_pedido, total) VALUES
(1, '2023-08-01', 1300.00),
(2, '2023-08-05', 270.00),
(3, '2023-08-10', 500.00),
(4, '2023-08-20', 250.00),
(5, '2023-08-25', 1200.00);

INSERT INTO Detalle_Pedidos (pedido_id, producto_id, cantidad, precio_unitario) VALUES
(1, 1, 1, 1200.00),
(1, 2, 4, 25.00),
(2, 2, 2, 25.00),
(2, 3, 4, 45.00),
(3, 4, 2, 250.00),
(4, 5, 1, 150.00),
(5, 1, 1, 1200.00);

Obtén el nombre de los clientes que han realizado pedidos y el total de cada pedido.
SELECT c.nombre,p.total 
from Clientes c join Pedidos p on c.cliente_id=p.cliente_id;

Encuentra los productos cuyo precio es mayor que el precio promedio de todos 
los productos
select *
from Productos p1 
where p1.precio >(
    Select AVG(p.precio)
    from Productos p);

Muestra el total de pedidos realizados por cada cliente, pero solo aquellos 
clientes que han realizado más de 3 pedidos.
SELECT c.nombre, COUNT(p.pedido_id) AS total_pedidos
FROM Clientes c
JOIN Pedidos p ON c.cliente_id = p.cliente_id
GROUP BY c.cliente_id
HAVING COUNT(p.pedido_id) > 3;

Calcula el total de ventas por producto y ordena los resultados de mayor a menor.
SELECT pr.nombre_producto, SUM(dp.cantidad * dp.precio_unitario) AS total_ventas
FROM Detalle_Pedidos dp JOIN Productos pr ON dp.producto_id = pr.producto_id
GROUP BY pr.producto_id
ORDER BY total_ventas DESC;

Encuentra los nombres de los productos que han sido comprados en cantidades superiores 
al promedio de cantidades de todos los productos.
SELECT nombre_producto
FROM Productos pr
WHERE pr.producto_id IN (
    SELECT producto_id
    FROM Detalle_Compras dc
    GROUP BY producto_id
    HAVING SUM(dc.cantidad) > (SELECT AVG(cantidad) FROM Detalle_Compras)
);

Encuentra los clientes que han comprado todos los productos disponibles en la 
base de datos.
SELECT c.nombre
FROM Clientes c
WHERE NOT EXISTS (
    SELECT 1
    FROM Productos p
    WHERE NOT EXISTS (
        SELECT 1
        FROM Detalle_Pedidos dp
        JOIN Pedidos p2 ON dp.pedido_id = p2.pedido_id
        WHERE dp.producto_id = p.producto_id AND p2.cliente_id = c.cliente_id
    )
);

Muestra el nombre y el total de todos los pedidos realizados por los clientes que han
realizado más de un pedido.
SELECT c.nombre, SUM(p.total) AS total_pedidos
FROM Pedidos p JOIN Clientes c ON p.cliente_id = c.cliente_id
GROUP BY c.cliente_id
HAVING COUNT(p.pedido_id) > 1;

Obtén el nombre del proveedor que más ha suministrado productos a la empresa,
junto con el total de productos suministrados.
