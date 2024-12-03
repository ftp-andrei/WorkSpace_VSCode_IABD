/*PASO 1*/
-------------------
/*

docker run --name MysqlDBA -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=Instituto -d mysql

docker ps

docker exec -it MysqlDBA bin/bash

mysql -u root -p

añadimos pass my-secret-pw

show databases;

use Instituto;

*/

/*
**** TABLAS ****
*/
CREATE TABLE Departamento (
    DepartmentID int NOT NULL PRIMARY KEY,
    DepartmentName nvarchar(255)
);

CREATE TABLE Profesor (
    ProfesorID int NOT NULL PRIMARY KEY,
    Nombre nvarchar(255),
    Apellido nvarchar(255),
    DepartmentID int,
    CONSTRAINT FK_Profesor_Departamento FOREIGN KEY (DepartmentID) REFERENCES Departamento(DepartmentID)
);

CREATE TABLE Curso (
    CourseID int NOT NULL PRIMARY KEY,
    CourseName nvarchar(255),
    Credits int,
    ProfesorID int,
    DepartmentID int,
    CONSTRAINT FK_Curso_Profesor FOREIGN KEY (ProfesorID) REFERENCES Profesor(ProfesorID),
    CONSTRAINT FK_Curso_Departamento FOREIGN KEY (DepartmentID) REFERENCES Departamento(DepartmentID)
);

CREATE TABLE Estudiante (
    StudentID int NOT NULL PRIMARY KEY,
    FirstName nvarchar(255),
    LastName nvarchar(255),
    DateOfBirth DATETIME,
    CourseID int,
    CONSTRAINT FK_Estudiante_Curso FOREIGN KEY (CourseID) REFERENCES Curso(CourseID)
);

/*
**** DATOS  ****
*/

insert into Departamento (DepartmentID, DepartmentName) VALUES 
(1, 'Matemáticas'), 
(2, 'Fisica y Quimica'), 
(3, 'Astronomia'), 
(4, 'Musica'), 
(5, 'Geografia e Historia'), 
(6, 'Literatura'), 
(7, 'Idiomas'), 
(8, 'Informatica'), 
(9, 'Religion'), 
(10, 'Latin');

insert into Profesor (ProfesorID, Nombre, Apellido, DepartmentID) VALUES 
(1, 'Juan', 'Garcia', 1), 
(2, 'Maria', 'Lopez', 2), 
(3, 'Pedro', 'Martinez', 3), 
(4, 'Ana', 'Sánchez', 4), 
(5, 'Luis', 'González', 5), 
(6, 'Sofia', 'Pérez', 6), 
(7, 'Carlos', 'Rodriguez', 7), 
(8, 'Laura', 'Fernández', 8), 
(9, 'Miguel', 'Diaz', 9), 
(10, 'Elena', 'Ruiz', 10),
(11, 'Javier', 'Hernández', 1),
(12, 'Carmen', 'Torres', 3),
(13, 'Ricardo', 'Jiménez', 3),
(14, 'Isabel', 'Luna', 2),
(15, 'Antonio', 'Gomez', 3),
(16, 'Marta', 'Serrano', 7),
(17, 'Fernando', 'Vega', 7),
(18, 'Rosa', 'Molina', 7),
(19, 'Daniel', 'Ortega', 8),
(20, 'Sara', 'Castro', 9);

insert into Curso (CourseID, CourseName, Credits, ProfesorID, DepartmentID) VALUES
(1, 'Matemáticas Avanzadas', 3, 1, 1),
(2, 'Física Cuántica', 4, 2, 2),
(3, 'Astronomía', 3, 3, 3),
(4, 'Música Clásica', 2, 4, 4),
(5, 'Historia Antigua', 4, 5, 5),
(6, 'Literatura', 3, 6, 6),
(7, 'Inglés', 2, 7, 7),
(8, 'Programación 1', 4, 8, 8),
(9, 'Religion', 1, 9, 9),
(10, 'Latín', 3, 10, 10),
(11, 'Matemáticas Avanzadas', 3, 11, 1),
(12, 'Quimica', 4, 12, 2),
(13, 'Astronomía', 3, 13, 3),
(14, 'Teoria Musical', 2, 14, 4),
(15, 'Geografía 2', 4, 15, 5),
(16, 'Literatura', 3, 16, 6),
(17, 'Inglés', 2, 17, 7),
(18, 'Programación 2', 4, 18, 8),
(19, 'Religion', 1, 19, 9),
(20, 'Latín', 3, 20, 10);

insert into Estudiante (StudentID, FirstName, LastName, DateOfBirth, CourseID) VALUES
(1, 'Juan', 'Garcia', '1995-05-15', 1),
(2, 'Maria', 'Lopez', '1996-08-20', 2),
(3, 'Pedro', 'Martinez', '1994-02-10', 2),
(4, 'Ana', 'Sánchez', '1997-11-25', 7),
(5, 'Luis', 'González', '1995-09-26', 1),
(6, 'Sofia', 'Pérez', '1996-04-06', 18),
(7, 'Carlos', 'Rodriguez', '1994-07-27', 4),
(8, 'Laura', 'Fernández', '1997-01-18', 4),
(9, 'Miguel', 'Diaz', '1995-03-22', 5),
(10, 'Elena', 'Ruiz', '1996-06-28', 9),
(11, 'Javier', 'Hernández', '1994-10-07', 6),
(12, 'Carmen', 'Torres', '1997-12-14', 3),
(13, 'Ricardo', 'Jiménez', '1995-02-19', 7),
(14, 'Isabel', 'Luna', '1996-05-24', 17),
(15, 'Antonio', 'Gomez', '1994-08-29', 6),
(16, 'Marta', 'Serrano', '2001-11-05', 18),
(17, 'Fernando', 'Vega', '1995-01-10', 19),
(18, 'Rosa', 'Molina', '2001-11-01', 19),
(19, 'Daniel', 'Ortega', '1994-07-20', 20),
(20, 'Sara', 'Castro', '1997-10-25', 13),
(21, 'Qasim', 'Al-Ikbar', '1995-03-30', 1),
(22, 'Lope', 'De Vega', '1996-06-05', 3),
(23, 'Carmen', 'Medrano', '1994-09-10', 12),
(24, 'Pau', 'Cubarsi', '1997-12-30', 2),
(25, 'Brahim', 'Diaz', '2002-02-01', 3),
(26, 'Mustafa', 'Abqar', '1996-05-25', 3),
(27, 'Muhamad', 'El-Halil', '2000-08-30', 9),
(28, 'Mohamed', 'bin Zayed', '1961-03-11', 4),
(29, 'Salvador', 'Matamaros', '2002-01-10', 5),
(30, 'Marc', 'Marquez', '2004-04-13', 5),
(31, 'Valentin', 'Rossi', '1980-07-20', 6),
(32, 'Radu', 'Mitu', '1997-10-13', 6),
(33, 'Joao', 'Neves', '1995-11-30', 8),
(34, 'Junior', 'Neymar', '1996-06-05', 7),
(35, 'Cruz', 'Gomez', '1994-09-10', 8),
(36, 'Heraclio', 'Temandez', '1960-12-15', 5),
(37, 'Josefina', 'Perez', '1934-02-20', 5),
(38, 'Adonis', 'Martinez', '1944-05-17', 9),
(39, 'Jose', 'Chino', '1954-08-30', 3),
(40, 'Ismael', 'Sanchez', '1967-11-05', 5);

/*
**** MODIFICACION Y ELIMINACION DATOS ****
**/

UPDATE Estudiante SET CourseID = 13 WHERE StudentID = 1;

UPDATE Departamento SET DepartmentName = 'Lengua y Literatura' WHERE DepartmentID = 6;

UPDATE Curso SET CourseName = 'Lengua' WHERE CourseID = 16;

UPDATE Profesor SET Apellido = 'de la Fuente' WHERE ProfesorID = 2;

DELETE FROM Estudiante WHERE StudentID = 33;


/*
**** CONSULTAS ****
**/

1. Muestra todos los estudiantes y sus nombres completos.
SELECT CONCAT(FirstName, ' ', LastName) AS Nombre Completo FROM Estudiante;

2. Lista los cursos ofrecidos por un departamento específico, por ejemplo, el
Departamento de Matemáticas.
SELECT c.CourseName FROM Curso c
JOIN Departamento d ON c.DepartmentID = d.DepartmentID
WHERE d.DepartmentName = 'Matemáticas';

3. Obtén todos los profesores asociados a un departamento en particular,
como el Departamento de Informática.
SELECT p.Nombre, p.Apellido FROM Profesor p
JOIN Departamento d ON p.DepartmentID = d.DepartmentID
WHERE d.DepartmentName = 'Informatica';

4. Muestra los estudiantes matriculados en un curso específico, por ejemplo,
el curso de Matemáticas Avanzadas.
SELECT e.FirstName, e.LastName FROM Estudiante e
JOIN Curso c ON e.CourseID = c.CourseID
WHERE c.CourseName = 'Matemáticas Avanzadas';

5. Encuentra los cursos que no tienen ningún estudiante matriculado.
SELECT c.CourseName FROM Curso c
LEFT JOIN Estudiante e ON c.CourseID = e.CourseID
WHERE e.StudentID IS NULL;

6. Identifica a los profesores que imparten más de un curso.
SELECT p.Nombre, p.Apellido FROM Profesor p
JOIN Curso c ON p.ProfesorID = c.ProfesorID
GROUP BY p.ProfesorID HAVING COUNT(c.CourseID) > 1;

7. Muestra todos los estudiantes que nacieron en un mes determinado, como
en enero.
SELECT FirstName, LastName FROM Estudiante
WHERE MONTH(DateOfBirth) = 1;

8. Encuentra los cursos con el mayor número de créditos.
SELECT CourseName FROM Curso
WHERE Credits = (SELECT MAX(Credits) FROM Curso);

9. Encuentra a los estudiantes que no se han matriculado en ningún curso.
SELECT FirstName, LastName FROM Estudiante
WHERE StudentID NOT IN (SELECT StudentID FROM Estudiante);

10. Identifica los departamentos que no tienen ningún curso asociado.
SELECT DepartmentName FROM Departamento
WHERE DepartmentID NOT IN (SELECT DepartmentID FROM Curso);
