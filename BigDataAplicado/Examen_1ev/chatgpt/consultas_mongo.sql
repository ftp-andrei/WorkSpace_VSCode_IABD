Operador	Descripción	Ejemplo
$eq	Igual a	{ edad: { $eq: 30 }}
$gt	Mayor que	{ edad: { $gt: 25 }}
$gte	Mayor o igual que	{ edad: { $gte: 25 }}
$lt	Menor que	{ edad: { $lt: 25 }}
$lte	Menor o igual que	{ edad: { $lte: 25 }}
$ne	No igual a	{ edad: { $ne: 30 }}
$in	En un conjunto de valores	{ ciudad: { $in: ["Madrid", "Barcelona"] }}
$or	O	{ $or: [{ edad: 25 }, { ciudad: "Madrid" }] }
$and	Y	{ $and: [{ edad: { $gte: 25 } }, { ciudad: "Madrid" }] }

Autenticación de Usuarios

Puedes crear usuarios y asignar roles:

db.createUser({
  user: "usuario",
  pwd: "contraseña",
  roles: [{ role: "readWrite", db: "miBaseDeDatos" }]
});


--1. Encuentra los productos que tienen una cantidad de stock menor al umbral dado.


db.producto.aggregate([
    {
        $match: {
            stock: { $lt: 10 } // Filtra los productos con stock menor que 10
        }
    },
    {
        $project: {
            nombre: 1,
            stock: 1
        }
    }
]);
--2. Encuentra la cantidad total vendida de cada producto por mes.


db.pedido.aggregate([
    { 
        $unwind: "$productos" 
    },
    {
        $project: {
            producto_id: "$productos.producto_id",
            cantidad: "$productos.cantidad",
            fecha: { $month: "$fecha" },  // Extraemos el mes de la fecha del pedido
            año: { $year: "$fecha" }  // Extraemos el año de la fecha del pedido
        }
    },
    {
        $group: {
            _id: { producto_id: "$producto_id", mes: "$fecha", año: "$año" }, // Agrupamos por mes y año
            totalVendidos: { $sum: "$cantidad" }
        }
    },
    {
        $project: {
            _id: 0,
            producto_id: "$_id.producto_id",
            mes: "$_id.mes",
            año: "$_id.año",
            totalVendidos: 1
        }
    }
]);
--3. Encuentra los productos más caros de cada categoría.


db.producto.aggregate([
    {
        $group: {
            _id: "$categoria",  // Agrupamos por categoría
            productoMasCaro: { $max: "$precio" }  // Obtenemos el precio máximo por categoría
        }
    },
    {
        $lookup: {
            from: "producto",
            localField: "productoMasCaro",
            foreignField: "precio",
            as: "producto"
        }
    },
    {
        $project: {
            _id: 0,
            categoria: "$_id",
            productoMasCaro: { $first: "$producto.nombre" }  // Mostramos el nombre del producto más caro
        }
    }
]);
--4. Encuentra los proveedores con los productos más baratos en cada categoría.


db.producto.aggregate([
    {
        $group: {
            _id: "$categoria", // Agrupamos por categoría
            precioMinimo: { $min: "$precio" }  // Obtenemos el precio mínimo por categoría
        }
    },
    {
        $lookup: {
            from: "producto",
            localField: "precioMinimo",
            foreignField: "precio",
            as: "producto"
        }
    },
    {
        $lookup: {
            from: "proveedor",
            localField: "producto.proveedorId", // Supongo que cada producto tiene un proveedorId
            foreignField: "_id",
            as: "proveedor"
        }
    },
    {
        $project: {
            _id: 0,
            categoria: "$_id",
            proveedor: { $first: "$proveedor.nombre" }, // Nombre del proveedor
            precioMinimo: 1
        }
    }
]);
--5. Encuentra los productos más comprados por cada cliente.


db.pedido.aggregate([
    { $unwind: "$productos" },
    {
        $group: {
            _id: { cliente_id: "$cliente_id", producto_id: "$productos.producto_id" }, 
            totalComprado: { $sum: "$productos.cantidad" } // Total de productos comprados por cliente
        }
    },
    {
        $sort: { "totalComprado": -1 } // Ordenamos de mayor a menor cantidad comprada
    },
    {
        $group: {
            _id: "$_id.cliente_id", 
            productoMasComprado: { $first: "$_id.producto_id" },  // El producto más comprado
            totalComprado: { $first: "$totalComprado" }
        }
    },
    {
        $lookup: {
            from: "producto", 
            localField: "productoMasComprado",
            foreignField: "_id",
            as: "producto"
        }
    },
    {
        $project: {
            _id: 0,
            cliente_id: "$_id",
            productoMasComprado: { $first: "$producto.nombre" },
            totalComprado: 1
        }
    }
]);
--6. Encuentra los clientes que realizaron pedidos en todos los meses del año.


db.pedido.aggregate([
    {
        $project: {
            cliente_id: 1,
            mes: { $month: "$fecha" },  // Extraemos el mes del pedido
            año: { $year: "$fecha" }    // Extraemos el año del pedido
        }
    },
    {
        $group: {
            _id: { cliente_id: "$cliente_id", año: "$año" },  // Agrupamos por cliente y año
            meses: { $addToSet: "$mes" }  // Almacenamos los meses en los que el cliente hizo pedidos
        }
    },
    {
        $match: {
            "meses": { $size: 12 }  // Filtramos aquellos que hicieron pedidos en todos los meses (12 meses)
        }
    },
    {
        $project: {
            _id: 0,
            cliente_id: "$_id.cliente_id",
            año: "$_id.año"
        }
    }
]);
--7. Encuentra los productos más baratos de cada proveedor.


db.producto.aggregate([
    {
        $group: {
            _id: "$proveedorId",  // Agrupamos por proveedor
            productoMasBarato: { $min: "$precio" }  // Obtenemos el precio más bajo por proveedor
        }
    },
    {
        $lookup: {
            from: "producto",
            localField: "productoMasBarato",
            foreignField: "precio",
            as: "producto"
        }
    },
    {
        $project: {
            _id: 0,
            proveedorId: "$_id",
            productoMasBarato: { $first: "$producto.nombre" }
        }
    }
]);
--8. Encuentra el número de productos vendidos por cada proveedor.


db.pedido.aggregate([
    { $unwind: "$productos" },
    {
        $group: {
            _id: "$productos.producto_id",  // Agrupamos por producto
            cantidadVendida: { $sum: "$productos.cantidad" }
        }
    },
    {
        $lookup: {
            from: "producto",
            localField: "_id",
            foreignField: "_id",
            as: "producto"
        }
    },
    {
        $group: {
            _id: "$producto.proveedorId",  // Agrupamos por proveedorId
            totalVendidos: { $sum: "$cantidadVendida" }
        }
    },
    {
        $lookup: {
            from: "proveedor",
            localField: "_id",
            foreignField: "_id",
            as: "proveedor"
        }
    },
    {
        $project: {
            _id: 0,
            proveedor: { $first: "$proveedor.nombre" }, // Mostramos el nombre del proveedor
            totalVendidos: 1
        }
    }
]);


--1. Encuentra el total de ingresos por mes en el último año


db.pedido.aggregate([
    {
        $match: {
            fecha: { $gte: ISODate("2023-11-01T00:00:00Z") } // Filtrar los pedidos del último año
        }
    },
    {
        $unwind: "$productos" // Desenrollamos los productos de cada pedido
    },
    {
        $lookup: {
            from: "producto",
            localField: "productos.producto_id",
            foreignField: "_id",
            as: "producto"
        }
    },
    {
        $group: {
            _id: { $month: "$fecha" }, // Agrupamos por mes
            ingresos: { 
                $sum: { 
                    $multiply: ["$productos.cantidad", { $first: "$producto.precio" }] 
                }
            }
        }
    },
    {
        $sort: { _id: 1 } // Ordenamos los resultados por mes (ascendente)
    },
    {
        $project: {
            mes: "$_id", 
            ingresos: 1, 
            _id: 0
        }
    }
]);
--2. Encuentra los productos más vendidos en el último trimestre


db.pedido.aggregate([
    {
        $match: {
            fecha: { $gte: ISODate("2024-08-01T00:00:00Z") } // Filtrar por pedidos del último trimestre
        }
    },
    {
        $unwind: "$productos" // Desenrollamos los productos de cada pedido
    },
    {
        $group: {
            _id: "$productos.producto_id", // Agrupamos por ID de producto
            totalVendidos: { $sum: "$productos.cantidad" } // Sumamos la cantidad vendida por producto
        }
    },
    {
        $sort: { totalVendidos: -1 } // Ordenamos los productos por cantidad vendida (en orden descendente)
    },
    {
        $limit: 10 // Limitamos el resultado a los 10 productos más vendidos
    },
    {
        $lookup: {
            from: "producto", 
            localField: "_id", 
            foreignField: "_id", 
            as: "producto"
        }
    },
    {
        $project: {
            nombre: { $arrayElemAt: ["$producto.nombre", 0] }, 
            totalVendidos: 1,
            _id: 0
        }
    }
]);
--3. Encuentra los empleados con más ventas en el último trimestre


db.pedido.aggregate([
    {
        $match: {
            fecha: { $gte: ISODate("2024-08-01T00:00:00Z") } // Filtrar pedidos del último trimestre
        }
    },
    {
        $unwind: "$productos" // Desenrollar los productos de cada pedido
    },
    {
        $lookup: {
            from: "producto", 
            localField: "productos.producto_id", 
            foreignField: "_id", 
            as: "producto"
        }
    },
    {
        $group: {
            _id: "$atendidoPor", // Agrupar por empleado que atendió el pedido
            totalVentas: {
                $sum: { 
                    $multiply: ["$productos.cantidad", { $first: "$producto.precio" }] 
                }
            }
        }
    },
    {
        $sort: { totalVentas: -1 } // Ordenar por las ventas en orden descendente
    },
    {
        $limit: 5 // Limitar a los 5 empleados con más ventas
    },
    {
        $lookup: {
            from: "empleado", 
            localField: "_id", 
            foreignField: "_id", 
            as: "empleado"
        }
    },
    {
        $project: {
            nombreEmpleado: { $arrayElemAt: ["$empleado.nombre", 0] },
            totalVentas: 1,
            _id: 0
        }
    }
]);
--4. Encuentra los proveedores con más productos en stock


db.producto.aggregate([
    {
        $match: { stock: { $gte: 0 } } // Filtrar productos con stock positivo
    },
    {
        $group: {
            _id: "$proveedorId", // Agrupar por proveedor
            totalProductos: { $sum: 1 } // Contar la cantidad de productos de cada proveedor
        }
    },
    {
        $sort: { totalProductos: -1 } // Ordenar por cantidad de productos en stock
    },
    {
        $limit: 5 // Limitar a los 5 proveedores con más productos
    },
    {
        $lookup: {
            from: "proveedor", 
            localField: "_id", 
            foreignField: "_id", 
            as: "proveedor"
        }
    },
    {
        $project: {
            nombreProveedor: { $arrayElemAt: ["$proveedor.nombre", 0] },
            totalProductos: 1,
            _id: 0
        }
    }
]);
--5. Encuentra los productos más caros de cada categoría


db.producto.aggregate([
    {
        $group: {
            _id: "$categoria", // Agrupamos por categoría
            maxPrecio: { $max: "$precio" } // Obtenemos el precio máximo de cada categoría
        }
    },
    {
        $lookup: {
            from: "producto", 
            localField: "maxPrecio", 
            foreignField: "precio", 
            as: "producto"
        }
    },
    {
        $unwind: "$producto" // Desenrollar los detalles del producto
    },
    {
        $project: {
            categoria: "$_id", 
            nombreProducto: "$producto.nombre",
            maxPrecio: 1, 
            _id: 0
        }
    }
]);
--6. Encuentra los clientes que compraron más de 3 veces un mismo producto


db.pedido.aggregate([
    {
        $unwind: "$productos" // Desenrollamos los productos
    },
    {
        $group: {
            _id: { cliente_id: "$cliente_id", producto_id: "$productos.producto_id" }, // Agrupamos por cliente y producto
            totalCompras: { $sum: 1 } // Contamos cuántas veces un cliente compró un producto
        }
    },
    {
        $match: {
            totalCompras: { $gt: 3 } // Filtramos aquellos clientes que compraron más de 3 veces el mismo producto
        }
    },
    {
        $lookup: {
            from: "producto", 
            localField: "_id.producto_id", 
            foreignField: "_id", 
            as: "producto"
        }
    },
    {
        $lookup: {
            from: "cliente", 
            localField: "_id.cliente_id", 
            foreignField: "_id", 
            as: "cliente"
        }
    },
    {
        $project: {
            cliente: { $arrayElemAt: ["$cliente.nombre", 0] },
            producto: { $arrayElemAt: ["$producto.nombre", 0] },
            totalCompras: 1,
            _id: 0
        }
    }
]);
--7. Encuentra los empleados con menor salario en cada departamento


db.empleado.aggregate([
    {
        $group: {
            _id: "$departamento", // Agrupamos por departamento
            salarioMinimo: { $min: "$salario" } // Obtenemos el salario mínimo por departamento
        }
    },
    {
        $lookup: {
            from: "empleado", 
            localField: "salarioMinimo", 
            foreignField: "salario", 
            as: "empleado"
        }
    },
    {
        $unwind: "$empleado" // Desenrollamos los detalles del empleado
    },
    {
        $project: {
            departamento: "$_id", 
            nombreEmpleado: "$empleado.nombre",
            salarioMinimo: 1, 
            _id: 0
        }
    }
]);
--8. Encuentra el producto más barato por categoría


db.producto.aggregate([
    {
        $group: {
            _id: "$categoria", // Agrupamos por categoría
            minPrecio: { $min: "$precio" } // Obtenemos el precio mínimo por categoría
        }
    },
    {
        $lookup: {
            from: "producto", 
            localField: "minPrecio", 
            foreignField: "precio", 
            as: "producto"
        }
    },
    {
        $unwind: "$producto" // Desenrollamos el producto
    },
    {
        $project: {
            categoria: "$_id", 
            nombreProducto: "$producto.nombre",
            minPrecio: 1, 
            _id: 0
        }
    }
]);



-- 1. Encuentra los clientes que han realizado compras en más de 2 categorías

db.pedido.aggregate([
    {
        $unwind: "$productos" // Desenrollamos los productos
    },
    {
        $lookup: {
            from: "producto", 
            localField: "productos.producto_id", 
            foreignField: "_id", 
            as: "producto"
        }
    },
    {
        $group: {
            _id: "$cliente_id", // Agrupamos por cliente
            categoriasCompradas: { $addToSet: "$producto.categoria" } // Almacenamos las categorías compradas
        }
    },
    {
        $match: {
            "categoriasCompradas.2": { $exists: true } // Filtramos clientes que han comprado en más de 2 categorías
        }
    },
    {
        $lookup: {
            from: "cliente", 
            localField: "_id", 
            foreignField: "_id", 
            as: "cliente"
        }
    },
    {
        $project: {
            cliente: { $arrayElemAt: ["$cliente.nombre", 0] },
            categoriasCompradas: 1,
            _id: 0
        }
    }
]);
-- 2. Encuentra la cantidad total de productos vendidos por cada empleado

db.pedido.aggregate([
    {
        $unwind: "$productos" // Desenrollamos los productos de cada pedido
    },
    {
        $group: {
            _id: "$atendidoPor", // Agrupamos por el ID del empleado
            totalVendidos: { $sum: "$productos.cantidad" } // Sumamos la cantidad de productos vendidos
        }
    },
    {
        $lookup: {
            from: "empleado", 
            localField: "_id", 
            foreignField: "_id", 
            as: "empleado"
        }
    },
    {
        $project: {
            empleado: { $arrayElemAt: ["$empleado.nombre", 0] },
            totalVendidos: 1,
            _id: 0
        }
    }
]);
-- 3. Encuentra los productos que no han sido comprados por ningún cliente en el último mes

db.producto.aggregate([
    {
        $lookup: {
            from: "pedido",
            let: { productoId: "$_id" },
            pipeline: [
                {
                    $unwind: "$productos"
                },
                {
                    $match: {
                        $expr: { $eq: ["$productos.producto_id", "$$productoId"] },
                        fecha: { $gte: ISODate("2024-10-01T00:00:00Z") } // Filtrar por pedidos en el último mes
                    }
                }
            ],
            as: "compras"
        }
    },
    {
        $match: {
            "compras": { $size: 0 } // Filtrar productos que no fueron comprados
        }
    },
    {
        $project: {
            nombre: 1,
            _id: 0
        }
    }
]);
-- 4. Encuentra los productos más caros y los más baratos por categoría

db.producto.aggregate([
    {
        $group: {
            _id: "$categoria", // Agrupamos por categoría
            maxPrecio: { $max: "$precio" }, // Encontramos el precio máximo por categoría
            minPrecio: { $min: "$precio" }  // Encontramos el precio mínimo por categoría
        }
    },
    {
        $lookup: {
            from: "producto", 
            localField: "maxPrecio", 
            foreignField: "precio", 
            as: "productoMax"
        }
    },
    {
        $lookup: {
            from: "producto", 
            localField: "minPrecio", 
            foreignField: "precio", 
            as: "productoMin"
        }
    },
    {
        $unwind: { path: "$productoMax", preserveNullAndEmptyArrays: true }
    },
    {
        $unwind: { path: "$productoMin", preserveNullAndEmptyArrays: true }
    },
    {
        $project: {
            categoria: "$_id",
            maxPrecio: "$productoMax.nombre",
            minPrecio: "$productoMin.nombre",
            _id: 0
        }
    }
]);
-- 5. Encuentra los productos que han sido más solicitados por un cliente específico

db.pedido.aggregate([
    {
        $match: {
            cliente_id: ObjectId("ID_DEL_CLIENTE") // Reemplazar con el ID del cliente específico
        }
    },
    {
        $unwind: "$productos" // Desenrollamos los productos de cada pedido
    },
    {
        $group: {
            _id: "$productos.producto_id", // Agrupamos por ID de producto
            cantidadTotal: { $sum: "$productos.cantidad" } // Sumamos la cantidad de veces que un producto fue comprado
        }
    },
    {
        $sort: { cantidadTotal: -1 } // Ordenamos por cantidad total de productos solicitados
    },
    {
        $lookup: {
            from: "producto", 
            localField: "_id", 
            foreignField: "_id", 
            as: "producto"
        }
    },
    {
        $project: {
            nombreProducto: { $arrayElemAt: ["$producto.nombre", 0] },
            cantidadTotal: 1,
            _id: 0
        }
    }
]);
-- 6. Encuentra los empleados que no han vendido nada en los últimos 6 meses

db.pedido.aggregate([
    {
        $match: {
            fecha: { $gte: ISODate("2024-05-01T00:00:00Z") } // Filtrar por pedidos de los últimos 6 meses
        }
    },
    {
        $unwind: "$productos" // Desenrollamos los productos de cada pedido
    },
    {
        $group: {
            _id: "$atendidoPor", // Agrupamos por el ID del empleado
            totalVentas: { $sum: 1 } // Contamos las ventas realizadas por cada empleado
        }
    },
    {
        $match: {
            totalVentas: { $eq: 0 } // Filtramos empleados sin ventas
        }
    },
    {
        $lookup: {
            from: "empleado", 
            localField: "_id", 
            foreignField: "_id", 
            as: "empleado"
        }
    },
    {
        $project: {
            nombreEmpleado: { $arrayElemAt: ["$empleado.nombre", 0] },
            totalVentas: 1,
            _id: 0
        }
    }
]);
-- 7. Encuentra los productos con el mayor número de ventas en una fecha específica

db.pedido.aggregate([
    {
        $match: {
            fecha: { $gte: ISODate("2024-11-01T00:00:00Z"), $lt: ISODate("2024-11-02T00:00:00Z") } // Filtrar por una fecha específica
        }
    },
    {
        $unwind: "$productos" // Desenrollamos los productos de cada pedido
    },
    {
        $group: {
            _id: "$productos.producto_id", // Agrupamos por ID de producto
            totalVendidos: { $sum: "$productos.cantidad" } // Sumamos las cantidades vendidas
        }
    },
    {
        $sort: { totalVendidos: -1 } // Ordenamos por la cantidad de productos vendidos (en orden descendente)
    },
    {
        $limit: 10 // Limitar a los 10 productos más vendidos
    },
    {
        $lookup: {
            from: "producto", 
            localField: "_id", 
            foreignField: "_id", 
            as: "producto"
        }
    },
    {
        $project: {
            nombreProducto: { $arrayElemAt: ["$producto.nombre", 0] },
            totalVendidos: 1,
            _id: 0
        }
    }
]);
-- 8. Encuentra los productos más vendidos por categoría en el último trimestre

db.pedido.aggregate([
    {
        $match: {
            fecha: { $gte: ISODate("2024-08-01T00:00:00Z") } // Filtrar por el último trimestre
        }
    },
    {
        $unwind: "$productos" // Desenrollamos los productos de cada pedido
    },
    {
        $lookup: {
            from: "producto", 
            localField: "productos.producto_id", 
            foreignField: "_id", 
            as: "producto"
        }
    },
    {
        $group: {
            _id: { categoria: "$producto.categoria", producto_id: "$producto._id" }, // Agrupamos por categoría y producto
            cantidadVendida: { $sum: "$productos.cantidad" } // Sumamos las cantidades vendidas por producto
        }
    },
    {
        $sort: { cantidadVendida: -1 } // Ordenamos por cantidad vendida (en orden descendente)
    },
    {
        $limit: 10 // Limitar a los 10 productos más vendidos
    },
    {
        $lookup: {
            from: "producto", 
            localField: "_id.producto_id", 
            foreignField: "_id", 
            as: "producto"
        }
    },
    {
        $project: {
            nombreProducto: { $arrayElemAt: ["$producto.nombre", 0] },
            categoria: "$_id.categoria",
            cantidadVendida: 1,
            _id: 0
        }
    }
]);