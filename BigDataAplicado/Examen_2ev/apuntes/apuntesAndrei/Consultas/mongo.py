
# 1. Agrupar empleados por departamento y calcular el salario promedio de cada uno
db.empleados.aggregate([
  { $group: { _id: "$departamento", salarioPromedio: { $avg: "$salario" } } }
]);

# 2. Encontrar empleados con el segundo salario más alto en cada departamento
db.empleados.aggregate([
  { $sort: { departamento: 1, salario: -1 } },
  { $group: { _id: "$departamento", empleados: { $push: "$$ROOT" } } },
  { $project: { _id: 1, segundoSalario: { $arrayElemAt: ["$empleados", 1] } } }
]);

# 3. Obtener los 5 empleados con los salarios más altos
db.empleados.find({}, { nombre: 1, salario: 1 }).sort({ salario: -1 }).limit(5);

# 4. Contar el número de proyectos activos en el último año
db.proyectos.aggregate([
  { $match: { fechaInicio: { $gte: new Date(new Date().setFullYear(new Date().getFullYear() - 1)) } } },
  { $count: "proyectosActivos" }
]);

# 5. Encontrar empleados que no tienen ningún proyecto asignado
db.empleados.aggregate([
  { $lookup: { from: "proyectos", localField: "_id", foreignField: "empleadoId", as: "proyectos" } },
  { $match: { proyectos: { $size: 0 } } }
]);

# 6. Calcular la duración promedio de los proyectos completados
db.proyectos.aggregate([
  { $match: { fechaFin: { $exists: true } } },
  { $project: { duracionDias: { $divide: [{ $subtract: ["$fechaFin", "$fechaInicio"] }, 1000 * 60 * 60 * 24] } } },
  { $group: { _id: null, duracionPromedio: { $avg: "$duracionDias" } } }
]);

# 7. Encontrar empleados asignados a más de 3 proyectos
db.proyectos.aggregate([
  { $group: { _id: "$empleadoId", totalProyectos: { $sum: 1 } } },
  { $match: { totalProyectos: { $gt: 3 } } }
]);

# 8. Obtener el historial de cambios de salario ordenado por empleado y fecha
db.historialSalarios.aggregate([
  { $sort: { empleadoId: 1, fechaCambio: -1 } }
]);

# 9. Mostrar los proyectos cuyo total de horas trabajadas es mayor al promedio
db.proyecto_empleado.aggregate([
  { $group: { _id: "$proyectoId", totalHoras: { $sum: "$horasTrabajadas" } } },
  { $group: { _id: null, promedioHoras: { $avg: "$totalHoras" } } },
  { $lookup: { from: "proyectos", localField: "_id", foreignField: "_id", as: "detallesProyecto" } },
  { $match: { totalHoras: { $gt: "$promedioHoras" } } }
]);

# 10. Mostrar empleados que comenzaron en la misma fecha
db.empleados.aggregate([
  { $group: { _id: "$fechaContratacion", empleados: { $push: "$nombre" }, total: { $sum: 1 } } },
  { $match: { total: { $gt: 1 } } }
]);

# 11. Encontrar proyectos con más de 10 empleados asignados
db.proyecto_empleado.aggregate([
  { $group: { _id: "$proyectoId", totalEmpleados: { $sum: 1 } } },
  { $match: { totalEmpleados: { $gt: 10 } } }
]);

# 12. Calcular el porcentaje de empleados en cada departamento
db.empleados.aggregate([
  { $group: { _id: "$departamento", total: { $sum: 1 } } },
  { $group: { _id: null, totalEmpleados: { $sum: "$total" }, departamentos: { $push: "$$ROOT" } } },
  { $unwind: "$departamentos" },
  { $project: { departamento: "$departamentos._id", porcentaje: { $multiply: [{ $divide: ["$departamentos.total", "$totalEmpleados"] }, 100] } } }
]);

# 13. Crear una vista que relacione empleados y proyectos
# MongoDB no tiene vistas como tal, pero puedes guardar una consulta como una colección:

db.empleados.aggregate([
  { $lookup: { from: "proyecto_empleado", localField: "_id", foreignField: "empleadoId", as: "proyectos" } },
  { $out: "vistaEmpleadosProyectos" }
]);

# 14. Encontrar departamentos donde todos los empleados ganan más de 3000
db.empleados.aggregate([
  { $group: { _id: "$departamento", salarioMinimo: { $min: "$salario" } } },
  { $match: { salarioMinimo: { $gt: 3000 } } }
]);

# 15. Calcular el salario promedio y la mediana de salarios
db.empleados.aggregate([
  { $group: { _id: null, promedio: { $avg: "$salario" }, salarios: { $push: "$salario" } } },
  { $project: { promedio: 1, mediana: { $arrayElemAt: ["$salarios", { $divide: [{ $size: "$salarios" }, 2] }] } } }
]);

# 16. Encontrar empleados con el mayor salario en cada departamento
db.empleados.aggregate([
  { $sort: { departamento: 1, salario: -1 } },
  { $group: { _id: "$departamento", empleado: { $first: "$$ROOT" } } }
]);

# 17. Obtener empleados cuyo salario no ha cambiado en 2 años
db.historialSalarios.aggregate([
  { $group: { _id: "$empleadoId", ultimaFecha: { $max: "$fechaCambio" } } },
  { $match: { ultimaFecha: { $lte: new Date(new Date().setFullYear(new Date().getFullYear() - 2)) } } }
]);

# 18. Mostrar el historial de proyectos completados por duración
db.proyectos.aggregate([
  { $match: { fechaFin: { $exists: true } } },
  { $project: { nombre: 1, duracionDias: { $divide: [{ $subtract: ["$fechaFin", "$fechaInicio"] }, 1000 * 60 * 60 * 24] } } },
  { $sort: { duracionDias: -1 } }
]);

# 19. Calcular la suma de salarios por departamento
db.empleados.aggregate([
  { $group: { _id: "$departamento", sumaSalarios: { $sum: "$salario" } } }
]);

# 20. Buscar empleados que comparten el mismo salario
db.empleados.aggregate([
  { $group: { _id: "$salario", empleados: { $push: "$nombre" }, total: { $sum: 1 } } },
  { $match: { total: { $gt: 1 } } }
]);

# 21. Encontrar empleados cuyo salario es superior al promedio de su departamento
db.empleados.aggregate([
  { $group: { _id: "$departamento", salarioPromedio: { $avg: "$salario" } } },
  { $lookup: { from: "empleados", localField: "_id", foreignField: "departamento", as: "empleados" } },
  { $unwind: "$empleados" },
  { $match: { "empleados.salario": { $gt: "$salarioPromedio" } } },
  { $project: { nombre: "$empleados.nombre", salario: "$empleados.salario", departamento: "$_id" } }
]);

# 22. Obtener los proyectos con más empleados asignados y el detalle de los mismos
db.proyecto_empleado.aggregate([
  { $group: { _id: "$proyectoId", totalEmpleados: { $sum: 1 } } },
  { $sort: { totalEmpleados: -1 } },
  { $limit: 1 },
  { $lookup: { from: "proyectos", localField: "_id", foreignField: "_id", as: "proyecto" } }
]);