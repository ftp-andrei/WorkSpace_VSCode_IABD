docker run --name mysqlRafa -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=Libros -d mysql
Desglose de los parámetros:
--name mysqlRafa: Establece el nombre del contenedor como mysqlRafa.
-e MYSQL_ROOT_PASSWORD=my-secret-pw: Establece la contraseña del usuario root a my-secret-pw.
-e MYSQL_DATABASE=Libros: Crea automáticamente la base de datos llamada Libros.
-d: Ejecuta el contenedor en segundo plano (detached).
mysql: Especifica que el contenedor debe usar la imagen oficial de MySQL.
Otros ejemplos con variables de entorno opcionales:
Si prefieres utilizar otras variables de entorno mencionadas:

--Generar una contraseña aleatoria para root:

docker run --name mysqlRafa -e MYSQL_RANDOM_ROOT_PASSWORD=yes -e MYSQL_DATABASE=Libros -d mysql
--Dejar la contraseña de root vacía (NO RECOMENDADO para producción):

docker run --name mysqlRafa -e MYSQL_ALLOW_EMPTY_PASSWORD=yes -e MYSQL_DATABASE=Libros -d mysql
--Establecer un usuario y contraseña personalizados:

docker run --name mysqlRafa -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_USER=usuario -e MYSQL_PASSWORD=contraseña -e MYSQL_DATABASE=Libros -d mysql
--Forzar a cambiar la contraseña de root al primer login:

docker run --name mysqlRafa -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_ONETIME_PASSWORD=yes -e MYSQL_DATABASE=Libros -d mysql
Cualquiera de estos comandos debería funcionar dependiendo de las necesidades de tu entorno.

-- 1. Lista todos los departamentos.
SELECT * FROM Departamento;

-- 2. Muestra los nombres de los profesores y sus IDs.
SELECT ProfesorID, CONCAT(Nombre, ' ', Apellido) AS NombreCompleto FROM Profesor;

-- 3. Encuentra todos los estudiantes nacidos después del año 2000.
SELECT FirstName, LastName FROM Estudiante WHERE YEAR(DateOfBirth) > 2000;

-- 4. Lista los cursos y su cantidad de créditos.
SELECT CourseName, Credits FROM Curso;

-- 5. Muestra los nombres completos de los estudiantes y sus fechas de nacimiento.
SELECT CONCAT(FirstName, ' ', LastName) AS NombreCompleto, DateOfBirth FROM Estudiante;

-- 6. Obtén el número total de estudiantes.
SELECT COUNT(*) AS TotalEstudiantes FROM Estudiante;

-- 7. Muestra los nombres de los departamentos ordenados alfabéticamente.
SELECT DepartmentName FROM Departamento ORDER BY DepartmentName;

-- 8. Lista los profesores con su respectivo departamento.
SELECT CONCAT(p.Nombre, ' ', p.Apellido) AS Profesor, d.DepartmentName AS Departamento
FROM Profesor p JOIN Departamento d ON p.DepartmentID = d.DepartmentID;

-- 9. Muestra los cursos con más de 3 créditos.
SELECT CourseName FROM Curso WHERE Credits > 3;

-- 10. Encuentra los departamentos que tienen más de 2 profesores.
SELECT d.DepartmentName, COUNT(p.ProfesorID) AS TotalProfesores
FROM Departamento d JOIN Profesor p ON d.DepartmentID = p.DepartmentID
GROUP BY d.DepartmentID HAVING COUNT(p.ProfesorID) > 2;

-- 11. Muestra los estudiantes matriculados en el curso de 'Programación 1'.
SELECT e.FirstName, e.LastName FROM Estudiante e
JOIN Curso c ON e.CourseID = c.CourseID
WHERE c.CourseName = 'Programación 1';

-- 12. Encuentra los departamentos sin profesores asignados.
SELECT DepartmentName FROM Departamento
WHERE DepartmentID NOT IN (SELECT DISTINCT DepartmentID FROM Profesor);

-- 13. Lista todos los profesores con más de un curso asignado.
SELECT p.Nombre, p.Apellido FROM Profesor p
JOIN Curso c ON p.ProfesorID = c.ProfesorID
GROUP BY p.ProfesorID HAVING COUNT(c.CourseID) > 1;

-- 14. Muestra los estudiantes cuyo apellido contiene la letra 'z'.
SELECT FirstName, LastName FROM Estudiante WHERE LastName LIKE '%z%';

-- 15. Encuentra todos los estudiantes que no están matriculados en ningún curso.
SELECT FirstName, LastName FROM Estudiante
WHERE StudentID NOT IN (SELECT DISTINCT StudentID FROM Estudiante WHERE CourseID IS NOT NULL);

-- 16. Muestra los cursos que tienen el mismo profesor.
SELECT c1.CourseName AS Curso1, c2.CourseName AS Curso2, p.Nombre AS Profesor
FROM Curso c1
JOIN Curso c2 ON c1.ProfesorID = c2.ProfesorID AND c1.CourseID <> c2.CourseID
JOIN Profesor p ON c1.ProfesorID = p.ProfesorID;

-- 17. Lista los departamentos que tienen menos de 2 cursos.
SELECT d.DepartmentName, COUNT(c.CourseID) AS TotalCursos
FROM Departamento d LEFT JOIN Curso c ON d.DepartmentID = c.DepartmentID
GROUP BY d.DepartmentID HAVING COUNT(c.CourseID) < 2;

-- 18. Encuentra los profesores que trabajan en el departamento de 'Informatica'.
SELECT p.Nombre, p.Apellido FROM Profesor p
JOIN Departamento d ON p.DepartmentID = d.DepartmentID
WHERE d.DepartmentName = 'Informatica';

-- 19. Lista todos los cursos ordenados por créditos de manera descendente.
SELECT CourseName, Credits FROM Curso ORDER BY Credits DESC;

-- 20. Encuentra los estudiantes matriculados en más de un curso (si se permite múltiples asignaciones).
SELECT e.FirstName, e.LastName, COUNT(c.CourseID) AS TotalCursos
FROM Estudiante e
JOIN Curso c ON e.CourseID = c.CourseID
GROUP BY e.StudentID HAVING COUNT(c.CourseID) > 1;

-- 21. Muestra los nombres y apellidos de los profesores que no tienen cursos asignados.
SELECT p.Nombre, p.Apellido FROM Profesor p
WHERE p.ProfesorID NOT IN (SELECT DISTINCT ProfesorID FROM Curso);

-- 22. Encuentra todos los cursos del departamento de 'Matemáticas' que tengan más de 3 créditos.
SELECT c.CourseName FROM Curso c
JOIN Departamento d ON c.DepartmentID = d.DepartmentID
WHERE d.DepartmentName = 'Matemáticas' AND c.Credits > 3;

-- 23. Muestra los nombres completos de los estudiantes y el curso en el que están matriculados.
SELECT CONCAT(e.FirstName, ' ', e.LastName) AS NombreCompleto, c.CourseName
FROM Estudiante e LEFT JOIN Curso c ON e.CourseID = c.CourseID;

-- 24. Lista los departamentos con el número total de cursos ofrecidos.
SELECT d.DepartmentName, COUNT(c.CourseID) AS TotalCursos
FROM Departamento d LEFT JOIN Curso c ON d.DepartmentID = c.DepartmentID
GROUP BY d.DepartmentID;

-- 25. Encuentra el curso con el menor número de créditos.
SELECT CourseName FROM Curso
WHERE Credits = (SELECT MIN(Credits) FROM Curso);


Consultas Adicionales
-- Lista los profesores y los departamentos a los que están asignados:


SELECT p.Nombre, p.Apellido, d.DepartmentName 
FROM Profesor p 
JOIN Departamento d ON p.DepartmentID = d.DepartmentID;
-- Muestra el número total de estudiantes matriculados en cada curso:


SELECT c.CourseName, COUNT(e.StudentID) AS TotalEstudiantes 
FROM Curso c 
LEFT JOIN Estudiante e ON c.CourseID = e.CourseID 
GROUP BY c.CourseID;
-- Encuentra a los estudiantes más jóvenes (con la fecha de nacimiento más reciente):


SELECT FirstName, LastName, DateOfBirth 
FROM Estudiante 
WHERE DateOfBirth = (SELECT MAX(DateOfBirth) FROM Estudiante);
-- Obtén una lista de cursos ordenados por el número de estudiantes matriculados (de mayor a menor):


SELECT c.CourseName, COUNT(e.StudentID) AS TotalEstudiantes 
FROM Curso c 
LEFT JOIN Estudiante e ON c.CourseID = e.CourseID 
GROUP BY c.CourseID 
ORDER BY TotalEstudiantes DESC;
-- Lista los profesores que no están asignados a ningún curso:


SELECT p.Nombre, p.Apellido 
FROM Profesor p 
LEFT JOIN Curso c ON p.ProfesorID = c.ProfesorID 
WHERE c.CourseID IS NULL;
-- Encuentra los cursos con más de 3 créditos:


SELECT CourseName, Credits 
FROM Curso 
WHERE Credits > 3;
-- Muestra la cantidad de estudiantes por departamento:


SELECT d.DepartmentName, COUNT(e.StudentID) AS TotalEstudiantes 
FROM Departamento d 
JOIN Curso c ON d.DepartmentID = c.DepartmentID 
LEFT JOIN Estudiante e ON c.CourseID = e.CourseID 
GROUP BY d.DepartmentID;
-- Encuentra a los estudiantes con el mismo apellido que algún profesor:


SELECT e.FirstName, e.LastName 
FROM Estudiante e 
JOIN Profesor p ON e.LastName = p.Apellido;
-- Lista los estudiantes que cumplen años en un mes específico (por ejemplo, diciembre):


SELECT FirstName, LastName, DateOfBirth 
FROM Estudiante 
WHERE MONTH(DateOfBirth) = 12;
-- Encuentra el promedio de créditos por curso en cada departamento:


SELECT d.DepartmentName, AVG(c.Credits) AS PromedioCreditos 
FROM Departamento d 
JOIN Curso c ON d.DepartmentID = c.DepartmentID 
GROUP BY d.DepartmentID;
Consultas Avanzadas
-- Encuentra los cursos que tienen más estudiantes que el promedio de estudiantes por curso:


SELECT c.CourseName, COUNT(e.StudentID) AS TotalEstudiantes 
FROM Curso c 
LEFT JOIN Estudiante e ON c.CourseID = e.CourseID 
GROUP BY c.CourseID 
HAVING COUNT(e.StudentID) > (
    SELECT AVG(NumEstudiantes) 
    FROM (
        SELECT COUNT(StudentID) AS NumEstudiantes 
        FROM Estudiante 
        GROUP BY CourseID
    ) AS Subquery
);
-- Muestra los cursos impartidos por profesores de un departamento específico (e.g., Matemáticas):


SELECT c.CourseName 
FROM Curso c 
JOIN Profesor p ON c.ProfesorID = p.ProfesorID 
JOIN Departamento d ON p.DepartmentID = d.DepartmentID 
WHERE d.DepartmentName = 'Matemáticas';
-- Lista los departamentos que tienen más de 5 profesores asignados:


SELECT d.DepartmentName, COUNT(p.ProfesorID) AS TotalProfesores 
FROM Departamento d 
JOIN Profesor p ON d.DepartmentID = p.DepartmentID 
GROUP BY d.DepartmentID 
HAVING COUNT(p.ProfesorID) > 5;
-- Encuentra a los estudiantes nacidos después del año 2000:


SELECT FirstName, LastName, DateOfBirth 
FROM Estudiante 
WHERE YEAR(DateOfBirth) > 2000;
-- Muestra los nombres completos de los profesores junto con los cursos que imparten:


SELECT p.Nombre, p.Apellido, c.CourseName 
FROM Profesor p 
JOIN Curso c ON p.ProfesorID = c.ProfesorID;
-- Identifica los departamentos que tienen tanto cursos como estudiantes matriculados:


SELECT DISTINCT d.DepartmentName 
FROM Departamento d 
JOIN Curso c ON d.DepartmentID = c.DepartmentID 
JOIN Estudiante e ON c.CourseID = e.CourseID;
-- Encuentra los estudiantes asignados al curso con el mayor número de créditos:


SELECT e.FirstName, e.LastName 
FROM Estudiante e 
JOIN Curso c ON e.CourseID = c.CourseID 
WHERE c.Credits = (SELECT MAX(Credits) FROM Curso);
-- Muestra los profesores y el número de estudiantes que tienen en sus cursos:


SELECT p.Nombre, p.Apellido, COUNT(e.StudentID) AS TotalEstudiantes 
FROM Profesor p 
JOIN Curso c ON p.ProfesorID = c.ProfesorID 
LEFT JOIN Estudiante e ON c.CourseID = e.CourseID 
GROUP BY p.ProfesorID;
-- Encuentra el curso con el menor número de estudiantes matriculados:


SELECT c.CourseName 
FROM Curso c 
LEFT JOIN Estudiante e ON c.CourseID = e.CourseID 
GROUP BY c.CourseID 
ORDER BY COUNT(e.StudentID) ASC 
LIMIT 1;
-- Muestra todos los cursos que tienen exactamente 2 créditos:


SELECT CourseName 
FROM Curso 
WHERE Credits = 2;

-- 1. Encuentra los estudiantes nacidos después de una fecha específica (por ejemplo, 1 de enero de 2000):

SELECT FirstName, LastName, DateOfBirth 
FROM Estudiante 
WHERE DateOfBirth > '2000-01-01';
Descripción: Esta consulta devuelve los estudiantes nacidos después del 1 de enero de 2000.

-- 2. Muestra los cursos ofrecidos en un año específico (por ejemplo, 1997):

SELECT CourseName, Credits 
FROM Curso 
WHERE YEAR(CourseID) = 1997;