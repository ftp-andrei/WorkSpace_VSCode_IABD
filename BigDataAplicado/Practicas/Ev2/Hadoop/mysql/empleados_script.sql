-- Usa la base de datos
USE hadoop;

-- Crea la tabla empleados
CREATE TABLE empleados (
    id INT PRIMARY KEY,
    nombre VARCHAR(50),
    departamento VARCHAR(50),
    salario DECIMAL(10,2),
    fecha_contratacion DATE
);
