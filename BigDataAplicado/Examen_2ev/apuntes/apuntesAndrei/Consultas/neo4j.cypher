
''' 1. Encontrar nodos con un atributo específico '''
MATCH (n:Empleado)
WHERE n.salario > 5000
RETURN n.nombre, n.salario;

''' 2. Contar el número de nodos de un tipo '''
MATCH (n:Proyecto)
RETURN COUNT(n) AS total_proyectos;

''' 3. Encontrar relaciones específicas entre nodos '''
MATCH (e:Empleado)-[r:TRABAJA_EN]->(p:Proyecto)
RETURN e.nombre, p.nombre, r.horas_trabajadas;

''' 4. Obtener empleados que trabajan en proyectos de un cliente específico '''
MATCH (e:Empleado)-[:TRABAJA_EN]->(p:Proyecto)-[:ASIGNADO_A]->(c:Cliente {nombre: "Empresa XYZ"})
RETURN e.nombre, p.nombre;

''' 5. Encontrar nodos sin relaciones '''
MATCH (e:Empleado)
WHERE NOT (e)-[:TRABAJA_EN]->()
RETURN e.nombre;

''' 6. Obtener la cantidad de relaciones por tipo '''
MATCH ()-[r]->()
RETURN TYPE(r) AS tipo_relacion, COUNT(r) AS total;

''' 7. Calcular el salario promedio de todos los empleados '''
MATCH (e:Empleado)
RETURN AVG(e.salario) AS salario_promedio;

''' 8. Encontrar empleados con el salario más alto '''
MATCH (e:Empleado)
RETURN e.nombre, e.salario
ORDER BY e.salario DESC
LIMIT 1;

''' 9. Obtener todos los nodos conectados directamente a un nodo específico '''
MATCH (n:Empleado {nombre: "Carlos"})--(conectado)
RETURN conectado;

''' 10. Contar el número de proyectos en los que participa cada empleado '''
MATCH (e:Empleado)-[:TRABAJA_EN]->(p:Proyecto)
RETURN e.nombre, COUNT(p) AS total_proyectos;

''' 11. Mostrar empleados que comparten el mismo proyecto '''
MATCH (e1:Empleado)-[:TRABAJA_EN]->(p:Proyecto)<-[:TRABAJA_EN]-(e2:Empleado)
WHERE e1 <> e2
RETURN e1.nombre, e2.nombre, p.nombre;

''' 12. Encontrar empleados que trabajan en proyectos activos '''
MATCH (e:Empleado)-[:TRABAJA_EN]->(p:Proyecto {estado: "Activo"})
RETURN e.nombre, p.nombre;

''' 13. Obtener los proyectos más populares (con más empleados asignados) '''
MATCH (p:Proyecto)<-[:TRABAJA_EN]-(e:Empleado)
RETURN p.nombre, COUNT(e) AS total_empleados
ORDER BY total_empleados DESC
LIMIT 1;

''' 14. Encontrar el camino más corto entre dos empleados '''
MATCH p = shortestPath((e1:Empleado {nombre: "Ana"})-[*]-(e2:Empleado {nombre: "Luis"}))
RETURN p;

''' 15. Mostrar todos los departamentos y la cantidad de empleados '''
MATCH (d:Departamento)<-[:PERTENECE_A]-(e:Empleado)
RETURN d.nombre, COUNT(e) AS total_empleados;

''' 16. Crear una nueva relación entre nodos '''
MATCH (e:Empleado {nombre: "Carlos"}), (p:Proyecto {nombre: "Proyecto A"})
MERGE (e)-[:TRABAJA_EN {horas_trabajadas: 20}]->(p);

''' 17. Encontrar empleados que trabajan en todos los proyectos '''
MATCH (e:Empleado)-[:TRABAJA_EN]->(p:Proyecto)
WITH e, COUNT(p) AS proyectos_empleado
MATCH (p2:Proyecto)
WITH e, proyectos_empleado, COUNT(p2) AS total_proyectos
WHERE proyectos_empleado = total_proyectos
RETURN e.nombre;

''' 18. Mostrar todos los jefes y sus subordinados '''
MATCH (j:Jefe)<-[:REPORTA_A]-(e:Empleado)
RETURN j.nombre AS jefe, COLLECT(e.nombre) AS subordinados;

''' 19. Encontrar los proyectos con mayor duración '''
MATCH (p:Proyecto)
RETURN p.nombre, p.fecha_inicio, p.fecha_fin, duration.between(date(p.fecha_inicio), date(p.fecha_fin)).months AS meses_duracion
ORDER BY meses_duracion DESC;

''' 20. Obtener empleados cuyo salario está por encima del promedio '''
MATCH (e:Empleado)
WITH AVG(e.salario) AS salario_promedio
MATCH (e:Empleado)
WHERE e.salario > salario_promedio
RETURN e.nombre, e.salario;

''' 21. Contar relaciones entrantes y salientes de un nodo '''
MATCH (e:Empleado {nombre: "Carlos"})
RETURN SIZE((e)-->) AS relaciones_salientes, SIZE((e)<--) AS relaciones_entrantes;

''' 22. Mostrar nodos con múltiples tipos de relaciones '''
MATCH (n)-[r]->()
RETURN n, COLLECT(DISTINCT TYPE(r)) AS tipos_relaciones;

''' 23. Encontrar empleados que solo trabajan en proyectos con un cliente específico '''
MATCH (e:Empleado)-[:TRABAJA_EN]->(p:Proyecto)-[:ASIGNADO_A]->(c:Cliente {nombre: "Empresa XYZ"})
WHERE NOT (e)-[:TRABAJA_EN]->(:Proyecto)-[:ASIGNADO_A]->(c2:Cliente) WHERE c2.nombre <> "Empresa XYZ"
RETURN e.nombre;

''' 24. Listar los proyectos terminados en el último año '''
MATCH (p:Proyecto)
WHERE date(p.fecha_fin) > date() - duration({months: 12})
RETURN p.nombre, p.fecha_fin;

''' 25. Eliminar nodos y relaciones de proyectos inactivos '''
MATCH (p:Proyecto {estado: "Inactivo"})-[r]-()
DELETE r, p;

''' 26. Encontrar empleados que cambiaron de departamento '''
MATCH (e:Empleado)-[:PERTENECIO_A]->(d1:Departamento), (e)-[:PERTENECE_A]->(d2:Departamento)
WHERE d1 <> d2
RETURN e.nombre, d1.nombre AS departamento_anterior, d2.nombre AS departamento_actual;

''' 27. Crear una relación jerárquica de empleados '''
MATCH (e1:Empleado {nombre: "Luis"}), (e2:Empleado {nombre: "Carlos"})
MERGE (e1)-[:SUPERVISA]->(e2);

''' 28. Calcular la cantidad de proyectos asignados por cada cliente '''
MATCH (c:Cliente)<-[:ASIGNADO_A]-(p:Proyecto)
RETURN c.nombre, COUNT(p) AS total_proyectos;

''' 29. Mostrar la jerarquía de empleados en un departamento '''
MATCH (d:Departamento {nombre: "IT"})<-[:PERTENECE_A]-(e:Empleado)-[:SUPERVISA*]->(sub:Empleado)
RETURN e.nombre AS jefe, COLLECT(sub.nombre) AS subordinados;

''' 30. Encontrar nodos duplicados según un atributo '''
MATCH (e:Empleado)
WITH e.nombre AS nombre, COLLECT(e) AS duplicados
WHERE SIZE(duplicados) > 1
RETURN nombre, duplicados;