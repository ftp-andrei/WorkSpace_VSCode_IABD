/*PASO 1*/
-------------------
/*

docker run --name mysqlPractica -e MYSQL_ROOT_PASSWORD=secret -e MYSQL_DATABASE=Instituto -d mysql

docker ps

docker exec -it mysqlPractica bin/bash

mysql -u root -p

añadimos pass secret

show databases;

use Instituto;

*/
CREATE TABLE Estudiante (
    StudentID int NOT NULL PRIMARY KEY,
    FirstName nvarchar(255),
    LastName nvarchar(255),
    DateOfBirth DATETIME,
    CONSTRAINT FK_Estudiante_Curso FOREIGN KEY (CourseID) REFERENCES Curso(CourseID)
);

CREATE TABLE Curso (
    CourseID int NOT NULL PRIMARY KEY,
    CourseName nvarchar(255),
    Credits int,
    CONSTRAINT FK_Curso_Profesor FOREIGN KEY (ProfesorID) REFERENCES Profesor(ProfesorID)
);

CREATE TABLE Profesor (
    ProfesorID int NOT NULL PRIMARY KEY,
    Nombre nvarchar(255),
    Apellido int,
    CONSTRAINT FK_Profesor_Departamento FOREIGN KEY (DepartmentID) REFERENCES Departamento(DepartmentID)
);

CREATE TABLE Departamento (
    DepartmentID int NOT NULL PRIMARY KEY,
    DepartmentName nvarchar(255)
);


