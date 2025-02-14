
-- 1. Seleccionar empleados con el salario más bajo en cada departamento
SELECT nombre, salario, departamento 
FROM empleados 
WHERE salario = (SELECT MIN(salario) FROM empleados e2 WHERE e2.departamento = empleados.departamento);

-- 2. Calcular la media, mediana y desviación estándar de los salarios
SELECT AVG(salario) AS promedio, 
       STDDEV(salario) AS desviacion_estandar
FROM empleados;

-- 3. Mostrar el empleado con más años en la empresa
SELECT nombre, DATEDIFF(CURDATE(), fecha_contratacion) AS años_en_empresa 
FROM empleados 
ORDER BY años_en_empresa DESC 
LIMIT 1;

-- 4. Contar el número de empleados por rango salarial
SELECT 
  CASE 
    WHEN salario < 2000 THEN 'Bajo'
    WHEN salario BETWEEN 2000 AND 5000 THEN 'Medio'
    ELSE 'Alto'
  END AS rango_salarial, 
  COUNT(*) AS total_empleados
FROM empleados
GROUP BY rango_salarial;

-- 5. Encontrar departamentos con al menos 10 empleados
SELECT departamento, COUNT(*) AS total_empleados 
FROM empleados 
GROUP BY departamento 
HAVING COUNT(*) >= 10;

-- 6. Mostrar proyectos que no tienen empleados asignados
SELECT nombre 
FROM proyectos 
WHERE id NOT IN (SELECT DISTINCT proyecto_id FROM asignacion_proyectos);

-- 7. Seleccionar los nombres de empleados y proyectos donde el empleado es responsable del proyecto
SELECT empleados.nombre AS empleado, proyectos.nombre AS proyecto 
FROM proyectos 
JOIN empleados ON proyectos.responsable_id = empleados.id;

-- 8. Contar empleados por tipo de contrato
SELECT tipo_contrato, COUNT(*) AS total_empleados 
FROM empleados 
GROUP BY tipo_contrato;

-- 9. Mostrar el total de horas trabajadas por cada empleado
SELECT empleados.nombre, SUM(asignacion_proyectos.horas_trabajadas) AS total_horas 
FROM empleados 
JOIN asignacion_proyectos ON empleados.id = asignacion_proyectos.empleado_id 
GROUP BY empleados.id;

-- 10. Mostrar empleados que no tienen un jefe asignado
SELECT nombre 
FROM empleados 
WHERE jefe_id IS NULL;

-- 11. Obtener el salario promedio por departamento
SELECT departamento, AVG(salario) AS salario_promedio 
FROM empleados 
GROUP BY departamento;

-- 12. Seleccionar los empleados con salarios únicos en la empresa
SELECT nombre, salario 
FROM empleados 
GROUP BY salario 
HAVING COUNT(*) = 1;

-- 13. Encontrar los empleados que trabajan en proyectos activos
SELECT DISTINCT empleados.nombre 
FROM empleados 
JOIN asignacion_proyectos ON empleados.id = asignacion_proyectos.empleado_id 
JOIN proyectos ON asignacion_proyectos.proyecto_id = proyectos.id 
WHERE proyectos.estado = 'Activo';

-- 14. Calcular la duración de cada proyecto en semanas
SELECT nombre, CEIL(DATEDIFF(fecha_fin, fecha_inicio) / 7) AS duracion_semanas 
FROM proyectos 
WHERE fecha_fin IS NOT NULL;

-- 15. Mostrar empleados que ganan más que su jefe
SELECT e1.nombre AS empleado, e1.salario AS salario_empleado, e2.salario AS salario_jefe 
FROM empleados e1 
JOIN empleados e2 ON e1.jefe_id = e2.id 
WHERE e1.salario > e2.salario;

-- 16. Listar los proyectos con más de 5 empleados asignados
SELECT proyectos.nombre, COUNT(asignacion_proyectos.empleado_id) AS total_empleados 
FROM proyectos 
JOIN asignacion_proyectos ON proyectos.id = asignacion_proyectos.proyecto_id 
GROUP BY proyectos.id 
HAVING COUNT(asignacion_proyectos.empleado_id) > 5;

-- 17. Encontrar el proyecto más antiguo
SELECT nombre, fecha_inicio 
FROM proyectos 
ORDER BY fecha_inicio ASC 
LIMIT 1;

-- 18. Mostrar empleados contratados en el último mes
SELECT nombre, fecha_contratacion 
FROM empleados 
WHERE fecha_contratacion >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH);

-- 19. Encontrar departamentos sin empleados
SELECT nombre 
FROM departamentos 
WHERE id NOT IN (SELECT DISTINCT departamento_id FROM empleados);

-- 20. Mostrar el número de empleados contratados por año
SELECT YEAR(fecha_contratacion) AS anio, COUNT(*) AS total_empleados 
FROM empleados 
GROUP BY YEAR(fecha_contratacion);

-- 21. Encontrar el jefe con más subordinados
SELECT jefe_id, COUNT(*) AS total_subordinados 
FROM empleados 
WHERE jefe_id IS NOT NULL 
GROUP BY jefe_id 
ORDER BY total_subordinados DESC 
LIMIT 1;

-- 22. Mostrar empleados cuyo salario es igual al promedio del departamento
SELECT nombre, salario, departamento 
FROM empleados e1 
WHERE salario = (SELECT AVG(salario) FROM empleados e2 WHERE e2.departamento = e1.departamento);

-- 23. Calcular la duración promedio de empleo en la empresa
SELECT AVG(DATEDIFF(CURDATE(), fecha_contratacion)) AS duracion_promedio 
FROM empleados;

-- 24. Mostrar proyectos que terminaron en el último trimestre
SELECT nombre, fecha_fin 
FROM proyectos 
WHERE fecha_fin BETWEEN DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND CURDATE();

-- 25. Encontrar los departamentos con el salario promedio más alto
SELECT departamento, AVG(salario) AS salario_promedio 
FROM empleados 
GROUP BY departamento 
ORDER BY salario_promedio DESC 
LIMIT 1;

-- 26. Obtener los nombres de empleados que trabajan en todos los proyectos
SELECT empleados.nombre 
FROM empleados 
JOIN asignacion_proyectos ON empleados.id = asignacion_proyectos.empleado_id 
GROUP BY empleados.id 
HAVING COUNT(DISTINCT proyecto_id) = (SELECT COUNT(*) FROM proyectos);

-- 27. Mostrar el historial de cambios de departamento para cada empleado
SELECT empleado_id, departamento_anterior, nuevo_departamento, fecha_cambio 
FROM historial_departamentos 
ORDER BY fecha_cambio DESC;

-- 28. Listar clientes con más de un proyecto asignado
SELECT clientes.nombre, COUNT(proyectos.id) AS total_proyectos 
FROM clientes 
JOIN proyectos ON clientes.id = proyectos.cliente_id 
GROUP BY clientes.id 
HAVING COUNT(proyectos.id) > 1;

-- 29. Calcular la tasa de empleados que dejaron la empresa por año
SELECT YEAR(fecha_salida) AS anio, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM empleados) AS tasa_salida 
FROM empleados 
WHERE fecha_salida IS NOT NULL 
GROUP BY YEAR(fecha_salida);

-- 30. Identificar empleados que nunca han cambiado de jefe
SELECT nombre 
FROM empleados 
WHERE id NOT IN (SELECT empleado_id FROM historial_jefes);
