-- SQL TEXTO 2
CREATE DATABASE Empresa; (?)
SHOW DATABASES;
USE Empresa;

-- CREACION TABLAS

CREATE TABLE Cliente(
    ClienteID int NOT NULL PRIMARY KEY,
    Nombre nvarchar(255),
    Email nvarchar(255)
);

CREATE TABLE Proyecto(
    ProyectoID int NOT NULL PRIMARY KEY,
    Nombre nvarchar(255),
    ClienteID int,
    FechaEntrega DATETIME,
    Presupuesto DECIMAL(10,2),
    CONSTRAINT FK_Proyecto_Cliente FOREIGN KEY (ClienteID) REFERENCES Cliente(ClienteID)
);

CREATE TABLE TipoMaquina(
    TipoID int NOT NULL PRIMARY KEY,
    Nombre nvarchar(255)
);

CREATE TABLE Maquina(
    MaquinaID int NOT NULL PRIMARY KEY,
    Nombre nvarchar(255),
    TipoID int,
    Temperatura DECIMAL(10,2),
    Vibracion DECIMAL(10,2),
    Consumo DECIMAL(10,2),
    Presion DECIMAL(10,2),
    Sensor nvarchar(255),
    CONSTRAINT FK_Maquina_Tipo FOREIGN KEY (TipoID) REFERENCES TipoMaquina(TipoID)
);

CREATE TABLE Empleado(
    EmpleadoID int NOT NULL PRIMARY KEY,
    Nombre nvarchar(255),
    Ciudad nvarchar(255)
);

CREATE TABLE Proyecto_Empleado(
    ProyectoEmpleadoID int AUTO_INCREMENT PRIMARY KEY,
    ProyectoID int,
    EmpleadoID int,
    NumHorasTrabajadas int,
    NumTareasEntregadas int,
    CONSTRAINT FK_ProyectoEmpleado_Proyecto FOREIGN KEY (ProyectoID) REFERENCES Proyecto(ProyectoID),
    CONSTRAINT FK_ProyectoEmpleado_Empleado FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID)
);
-- Se podría haber añadido un campo de "Entregado" en Tarea_Proyecto, respondiendo a Si/No
CREATE TABLE Tarea_Proyecto(
    TareaID int AUTO_INCREMENT PRIMARY KEY,
    Nombre nvarchar(255),
    Descripcion nvarchar(255),
    ProyectoID int,
    EmpleadoID int,
    CONSTRAINT FK_Empleado_Tarea FOREIGN KEY (EmpleadoID) REFERENCES Empleado(EmpleadoID),
    CONSTRAINT FK_Proyecto_Tarea FOREIGN KEY (ProyectoID) REFERENCES Proyecto(ProyectoID)
);

-- INSERCION DATOS

INSERT INTO Cliente(ClienteID,Nombre,Email) VALUES 
(1, 'Jesus','jesus@hotmail.com'),
(2, 'Juan','juan@hotmail.com'),
(3, 'Pedro','pedro@hotmail.com'),
(4, 'Maria','maria@hotmail.com'),
(5, 'Jose','jose@hotmail.com'),
(6, 'Vicente','vicente@hotmail.com'),
(7, 'Samuel','samuel@hotmail.com'),
(8, 'Paula','paula@hotmail.com'),
(9, 'Sebastian','sebastian@hotmail.com'),
(10, 'Socrates','socrates@hotmail.com');

INSERT INTO Proyecto(ProyectoID,Nombre,ClienteID,FechaEntrega,Presupuesto) VALUES 
(1, 'Proyecto1',1,'2024-12-12', 500.00),
(2, 'Proyecto2',2,'2024-12-11', 1000.50),
(3, 'Proyecto3',3,'2024-12-10', 3243.30),
(4, 'Proyecto4',4,'2024-11-12', 1000.50),
(5, 'Proyecto5',5,'2024-10-12', 800.21),
(6, 'Proyecto6',6,'2024-9-12', 900.12),
(7, 'Proyecto7',7,'2024-01-12', 2300.19),
(8, 'Proyecto8',8,'2024-05-12', 6123.50),
(9, 'Proyecto9',9,'2024-07-12', 10000.01),
(10, 'Proyecto10',10,'2024-12-12', 777.77);

-- Liadita aqui perdon jaja. 
-- INSERT INTO TipoMaquina(TipoID, Nombre) VALUES
-- (1, 'Tipo1'),
-- (2, 'Tipo2'),
-- (3, 'Tipo3'),
-- (4, 'Tipo4'),
-- (5, 'Tipo5'),
-- (6, 'Tipo6'),
-- (7, 'Tipo7'),
-- (8, 'Tipo8'),
-- (9, 'Tipo9'),
-- (10, 'Tipo10');

-- INSERT INTO Maquina(MaquinaID,Nombre,TipoID,Temperatura,Vibracion,Consumo,Presion,Sensor) VALUES
-- (1, 'Maquina1',1,20.5,10.2,55.12,13.12,'Sensor1'),
-- (2, 'Maquina2',2,20.5,10.2,55.12,14.12,'Sensor2'),
-- (3, 'Maquina3',3,20.5,14.2,55.12,15.12,'Sensor3'),
-- (4, 'Maquina4',4,20.5,14.2,15.12,16.12,'Sensor4'),
-- (5, 'Maquina5',5,20.5,14.2,35.12,17.12,'Sensor5'),
-- (6, 'Maquina6',6,40.5,10.2,45.12,18.12,'Sensor6'),
-- (7, 'Maquina7',7,40.5,17.2,15.12,12.12,'Sensor7'),
-- (8, 'Maquina8',8,40.5,30.2,52.12,11.12,'Sensor8'),
-- (9, 'Maquina9',9,20.5,10.2,53.12,12.12,'Sensor9'),
-- (10, 'Maquina10',10,20.5,10.2,55.12,12.12,'Sensor10');


INSERT INTO Empleado(EmpleadoID,Nombre,Ciudad) VALUES 
(1, 'Sonia', 'Malaga'),
(2, 'Miguel', 'Logrono'),
(3, 'Fernando', 'Sevilla'),
(4, 'Mario', 'Oyon'),
(5, 'Hernando', 'Malaga'),
(6, 'Lucia', 'Malaga'),
(7, 'Ruben', 'Malaga'),
(8, 'Yeray', 'Malaga'),
(9, 'Luis', 'Malaga'),
(10, 'Javier', 'Malaga');


INSERT INTO Proyecto_Empleado(ProyectoID,EmpleadoID,NumHorasTrabajadas,NumTareasEntregadas) VALUES 
(1, 1, 10, 10),
(2, 1, 12, 44),
(3, 2, 13, 14),
(4, 3, 13, 14),
(5, 4, 15, 103),
(6, 5, 20, 110),
(7, 6, 40, 30),
(8, 7, 40, 50),
(9, 8, 60, 50),
(10, 9, 44, 60);


INSERT INTO Tarea_Proyecto(Nombre,Descripcion,ProyectoID,EmpleadoID) VALUES 
('Nombre1', 'Descripcion1',1,1),
('Nombre2', 'Descripcion2',2,2),
('Nombre3', 'Descripcion3',3,3),
('Nombre4', 'Descripcion4',4,4),
('Nombre5', 'Descripcion5',5,5),
('Nombre6', 'Descripcion6',6,6),
('Nombre7', 'Descripcion7',7,1),
('Nombre8', 'Descripcion8',8,2),
('Nombre9', 'Descripcion9',9,3),
('Nombre10', 'Descripcion10',10,3);


-- CONSULTAS

-- Mostrar los nombres de los proyectos junto con el nombre del cliente asociado.
SELECT p.nombre as NombreProyecto,c.nombre FROM Proyecto p JOIN Cliente c ON p.ClienteID=c.ClienteID;
-- Calcular el total de horas trabajadas por cada proyecto
SELECT p.nombre, SUM(pe.NumHorasTrabajadas) AS total_horas
FROM Proyecto p
JOIN Proyecto_Empleado pe ON p.ProyectoID = pe.ProyectoID
GROUP BY p.ProyectoID;
-- Encontrar los nombres de los proyectos cuyo total de horas trabajadas es mayor que el promedio de horas trabajadas en todos los proyectos
SELECT p.nombre, SUM(pe.NumHorasTrabajadas) AS total_horas 
FROM Proyecto p
JOIN Proyecto_Empleado pe ON p.ProyectoID = pe.ProyectoID
GROUP BY p.ProyectoID WHERE SUM(pe.NumHorasTrabajadas) > (SELECT avg(NumHorasTrabajadas) FROM Proyecto_Empleado);


-- MONGO TEXTO 3

-- CREAMOS/USAMOS LA BD
use PlantaIndustrial

-- CREAMOS LAS COLLECTION 

db.createCollection("maquina")
db.createCollection("sensor")
db.createCollection("alerta")

-- INSERTAMOS LOS DATOS

db.alerta.insertMany([
    {"Nombre": "Alerta1", "Descripcion": "Baja temperatura"},
    {"Nombre": "Alerta2", "Descripcion": "Presion alta"},
    {"Nombre": "Alerta3", "Descripcion": "Consumo alto"},
    {"Nombre": "Alerta4", "Descripcion": "Alta temperatura"},
    {"Nombre": "Alerta5", "Descripcion": "Presion baja"}
])

    '0': ObjectId('674a0ee1c2ef0deaa8fe6911'),
    '1': ObjectId('674a0ee1c2ef0deaa8fe6912'),
    '2': ObjectId('674a0ee1c2ef0deaa8fe6913'),
    '3': ObjectId('674a0ee1c2ef0deaa8fe6914'),
    '4': ObjectId('674a0ee1c2ef0deaa8fe6915')

-- Me di cuenta al final del examen: habría que haber hecho un array de alertas, por si salta alguna alerta más, como en la collection de maquina
db.sensor.insertMany([
    {"Nombre": "S001", "Temperatura": 10.33, "Vibraciones": "si", "Consumo": 55, "Presion": 10, "AlertaID": ObjectId('674a0ee1c2ef0deaa8fe6911')},
    {"Nombre": "S002", "Temperatura": 31.11, "Vibraciones": "no", "Consumo": 45, "Presion": 30, "AlertaID": ObjectId('674a0ee1c2ef0deaa8fe6912')},
    {"Nombre": "S003", "Temperatura": 23.33, "Vibraciones": "no", "Consumo": 35, "Presion": 50, "AlertaID": ObjectId('674a0ee1c2ef0deaa8fe6913')},
    {"Nombre": "S004", "Temperatura": 13.23, "Vibraciones": "no", "Consumo": 25, "Presion": 15, "AlertaID": ObjectId('674a0ee1c2ef0deaa8fe6914')},
    {"Nombre": "S005", "Temperatura": 9.11, "Vibraciones": "no", "Consumo": 15, "Presion": 44, "AlertaID": ObjectId('674a0ee1c2ef0deaa8fe6915')}
])

    '0': ObjectId('674a1001c2ef0deaa8fe6916'),
    '1': ObjectId('674a1001c2ef0deaa8fe6917'),
    '2': ObjectId('674a1001c2ef0deaa8fe6918'),
    '3': ObjectId('674a1001c2ef0deaa8fe6919'),
    '4': ObjectId('674a1001c2ef0deaa8fe691a')

db.maquina.insertMany([
    { "nombre": "Maquina1", "InstaladaEn": "Planta Baja", "Fabricante": "Ring", "FechaMantenimiento": ISODate("2022-03-18T11:36:01Z"), "Sensores": [{"Sensor1": ObjectId("674a1001c2ef0deaa8fe6916")}, {"Sensor2": ObjectId("674a1001c2ef0deaa8fe691a")}]} ,
    { "nombre": "Maquina2", "InstaladaEn": "Planta Superior", "Fabricante": "Tedy", "FechaMantenimiento": ISODate("2022-03-18T11:36:01Z"), "Sensores": [{"Sensor1": ObjectId("674a1001c2ef0deaa8fe6917")}, {"Sensor2": ObjectId("674a1001c2ef0deaa8fe6918")}]} ,
    { "nombre": "Maquina3", "InstaladaEn": "Planta 2", "Fabricante": "Mann", "FechaMantenimiento": ISODate("2021-04-18T11:36:01Z"), "Sensores": [{"Sensor1": ObjectId("674a1001c2ef0deaa8fe6918")}]} ,
    { "nombre": "Maquina4", "InstaladaEn": "Planta 3", "Fabricante": "Ring", "FechaMantenimiento": ISODate("2023-02-18T11:36:01Z"), "Sensores": [{"Sensor1": ObjectId("674a1001c2ef0deaa8fe6919")},{"Sensor2": ObjectId("674a1001c2ef0deaa8fe6916")}]} ,
    { "nombre": "Maquina5", "InstaladaEn": "Planta 6", "Fabricante": "Ring", "FechaMantenimiento": ISODate("2024-01-18T11:36:01Z"), "Sensores": [{"Sensor1": ObjectId("674a1001c2ef0deaa8fe691a")}, {"Sensor2": ObjectId("674a1001c2ef0deaa8fe6919")}]}
])


    '0': ObjectId('674a1142c2ef0deaa8fe691b'),
    '1': ObjectId('674a1142c2ef0deaa8fe691c'),
    '2': ObjectId('674a1142c2ef0deaa8fe691d'),
    '3': ObjectId('674a1142c2ef0deaa8fe691e'),
    '4': ObjectId('674a1142c2ef0deaa8fe691f')


-- CONSULTAS

1. Obtener todas las lecturas de un sensor específico, por ejemplo, "S001".
db.sensor.find({Nombre:'S001'})
2. Contar cuántos sensores están asociados a cada máquina.
db.maquina.aggregate([
    {
        $group: {
            _id: "$Sensores",   
            totalSensores: { $sum: 1 }
        }
    },
]);
3. Calcular cuántos sensores activos están asociados a cada máquina, incluyendo
los datos de la máquina, como su tipo y ubicación.



-- NEO4J

-- CONSULTAS

1. Listar todos los usuarios que han marcado un videojuego como favorito.
MATCH ()-[r:Marcado_Favorito]->()
RETURN r:
2. Obtener todos los videojuegos que han sido reseñados, incluyendo el título de la
reseña y el nombre del usuario que la escribió.
MATCH (v:Videojuego)-[:RESENADOS]->(r:Resena)
RETURN v.titulo, r.nomUser
3. Encontrar usuarios que siguen a otros usuarios que han reseñado un videojuego
específico, por ejemplo, "Elder Scrolls V: Skyrim", agrupando los resultados.


