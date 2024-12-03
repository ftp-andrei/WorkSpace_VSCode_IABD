docker run --name PracticaMongo -v Mongo_Practica:/data/db -e MONGO_INITDB_ROOT_USERNAME=mongoadmin -e MONGO_INITDB_ROOT_PASSWORD=secret -d mongo 

docker exec -it PracticaMongo bin/bash

mongosh -u mongoadmin -p secret --authenticationDatabase admin

--CREAMOS LA BD--
use tienda

--CREAMOS LAS COLECCIONES--
db.createCollection("producto")
db.createCollection("cliente")
db.createCollection("pedido")
db.createCollection("proveedor")

--Cambiamos valores--

db.producto.updateOne(
    {},
    { $set: { descripcion: "Algodon 50% poliester 50%" } }
);

db.proveedor.updateOne(
    { nombre: "HP" }, 
    { $set: { nombre: "NVIDIA" } } 
);

db.cliente.updateOne(
    { _id: ObjectId("67432f4500d0734e55499e56") },
    { $set: { telefono: 665658897 } }
);

db.empleado.updateOne(
    { _id: ObjectId("67432fd900d0734e55499e65") },
    { $set: { departamento: "Desarrollo de Software" } }
);

db.pedido.updateOne(
    { 
        _id: ObjectId("67433ce23ea0c7c849c1cd83"),
        "productos.producto_id": ObjectId("67432e5500d0734e55499e4f")
    },
    { 
        $set: { "productos.$.cantidad": 4 } 
    }
);

--INSERTAMOS LOS DATOS--
db.proveedor.insertMany([
    { "nombre": "Electronica Vicente"},
    { "nombre": "Coolmod"},
    { "nombre": "Corsair"},
    { "nombre": "Xiaomi"},
    { "nombre": "Calvin Klein"},
    { "nombre": "LaCoste"},
    { "nombre": "PC Box"},
    { "nombre": "Tedy S.L"},
    { "nombre": "PCComponentes"},
    { "nombre": "Logitech"},
    { "nombre": "HP"}
])

db.producto.insertMany([
      { "nombre": "Camiseta 1", "precio": 19.99, "descripcion": "Es de algodon", "categoria": "Ropa de vestir", "stock": 100, "proveedorId": ObjectId("6743299e00d0734e55499e3d") },
      { "nombre": "Pantalones Vaqueros", "precio": 30.00, "descripcion": "De buena calidad", "categoria": "Ropa de vestir", "stock": 55, "proveedorId": ObjectId("6743299e00d0734e55499e3d")  },
      { "nombre": "Zapatillas", "precio": 99.99, "descripcion": "Made in China", "categoria": "Calzado", "stock": 10, "proveedorId": ObjectId("6743299e00d0734e55499e3e")  },
      { "nombre": "Caramelos", "precio": 1.99, "descripcion": "Halls", "categoria": "Dulces", "stock": 14, "proveedorId": ObjectId("6743299e00d0734e55499e40")  },
      { "nombre": "Chicles", "precio": 0.99, "descripcion": "Trident", "categoria": "Dulces", "stock": 17, "proveedorId": ObjectId("6743299e00d0734e55499e40")  },
      { "nombre": "Bombones", "precio": 4.99, "descripcion": "Lindt", "categoria": "Chocolates & Surtidos", "stock": 22, "proveedorId": ObjectId("6743299e00d0734e55499e40")  },
      { "nombre": "Luces de navidad", "precio": 34.99, "descripcion": "Luces led 30m", "categoria": "Navidad", "stock": 25, "proveedorId": ObjectId("6743299e00d0734e55499e40")  },
      { "nombre": "Telefono", "precio": 499.95, "descripcion": "Xiaomi Redmi", "categoria": "Informatica", "stock": 10, "proveedorId": ObjectId("6743299e00d0734e55499e3f")  },
      { "nombre": "Ordenador", "precio": 999.95, "descripcion": "Gama alta, 4090ti + R9 7950X", "categoria": "Informatica", "stock": 1000, "proveedorId": ObjectId("6743299e00d0734e55499e3f")  },
      { "nombre": "Teclado", "precio": 69.98, "descripcion": "Mecanico switches red", "categoria": "Informatica", "stock": 500, "proveedorId": ObjectId("6743299e00d0734e55499e43")  },
      { "nombre": "Cable usb C", "precio": 6.95, "descripcion": "1,5M 30w", "categoria": "Informatica", "stock": 5000, "proveedorId": ObjectId("6743299e00d0734e55499e42")  },
      { "nombre": "Adornos navidad", "precio": 3.95, "descripcion": "Surtido variado adornos", "categoria": "Navidad", "stock": 40, "proveedorId": ObjectId("6743299e00d0734e55499e3f")  },
])

db.cliente.insertMany([
    { "nombre": "Juan", "correo": "juan@hotmail.com", "telefono": "633923759", "direccion": "Calle Madrid 1"},
    { "nombre": "Maria", "correo": "maria@hotmail.com", "telefono": "691029558", "direccion": "Avenida Buenos Aires 55"},
    { "nombre": "Pedro", "correo": "pedro@hotmail.com", "telefono": "690094562", "direccion": "Plaza Mayor"},
    { "nombre": "Ana", "correo": "ana@hotmail.com", "telefono": "612345678", "direccion": "Calle Benito Villamarin 3"},
    { "nombre": "Luis", "correo": "luis@hotmail.com", "telefono": "666943019", "direccion": "Avenida Portugal 7"},
    { "nombre": "Elena", "correo": "elena@hotmail.com", "telefono": "619203849", "direccion": "Plaza Central 66"},
    { "nombre": "Carlos", "correo": "carlos@hotmail.com", "telefono": "690945129", "direccion": "Calle San Marino 8"},
    { "nombre": "Sofia", "correo": "sofia@hotmail.com", "telefono": "784456769", "direccion": "Avenida Jose Marin 10"},
    { "nombre": "Miguel", "correo": "miguel@hotmail.com", "telefono": "6829304957", "direccion": "Plaza Eguizabal Iturrasbe 9"},
    { "nombre": "Laura", "correo": "laura@hotmail.com", "telefono": "694434697", "direccion": "Calle Rio Miño 2"},
    { "nombre": "Diego", "correo": "diego@hotmail.com", "telefono": "683759483", "direccion": "Avenida Solidaridad 33"},
    { "nombre": "Carmen", "correo": "carmen@hotmail.com", "telefono": "634556789", "direccion": "Plaza Guindalera 60"}
])

db.empleado.insertMany([
    { "nombre": "Juan", "departamento": "Ventas", "salario": 990.15, "fechaContratacion": ISODate("2022-03-18T11:36:01Z") }, 
    { "nombre": "Aitor", "departamento": "Inventario y Logistica", "salario": 1550.01, "fechaContratacion": ISODate("2019-11-13T08:34:15Z") }, 
    { "nombre": "Jose", "departamento": "RR.HH", "salario": 1350.47, "fechaContratacion": ISODate("2020-10-12T12:11:17Z") }, 
    { "nombre": "Ana", "departamento": "Seguridad", "salario": 1050.66, "fechaContratacion": ISODate("2020-09-10T13:12:18Z") }, 
    { "nombre": "Maria", "departamento": "RR.HH", "salario": 1750.97, "fechaContratacion": ISODate("2016-06-09T17:01:33Z") }, 
    { "nombre": "Fernando", "departamento": "Inventario y Logistica", "salario": 1550.44, "fechaContratacion": ISODate("2017-05-07T18:46:44Z") }, 
    { "nombre": "Millan", "departamento": "Ventas", "salario": 1230.77, "fechaContratacion": ISODate("2019-04-03T13:45:52Z") }, 
    { "nombre": "Sara", "departamento": "Ventas", "salario": 1110.25, "fechaContratacion": ISODate("2020-04-01T12:31:55Z") }, 
    { "nombre": "Mohamed", "departamento": "Ventas", "salario": 1100.11, "fechaContratacion": ISODate("2020-04-15T15:34:04Z") }, 
    { "nombre": "Manolo", "departamento": "Ventas", "salario": 1030.23, "fechaContratacion": ISODate("2022-01-22T09:23:03Z") }, 
    { "nombre": "Vicente", "departamento": "Soporte Tecnico", "salario": 1050.35, "fechaContratacion": ISODate("2022-08-23T08:12:11Z") }, 
])

db.pedido.insertMany([
    { "cliente_id": ObjectId("67432f4500d0734e55499e50"), "fecha": ISODate("2024-03-23T10:30:01Z"), "productos": [{"producto_id": ObjectId("67432e5500d0734e55499e44"), "cantidad": 4, "calificacion": 6}, {"producto_id": ObjectId("67432e5500d0734e55499e4f"), "cantidad": 1, "calificacion": 8}], "atendidoPor": ObjectId("67432fd900d0734e55499e5c") },
    { "cliente_id": ObjectId("67432f4500d0734e55499e51"), "fecha": ISODate("2024-05-11T11:31:30Z"), "productos": [{"producto_id": ObjectId("67432e5500d0734e55499e45"), "cantidad": 3, "calificacion": 7}, {"producto_id": ObjectId("67432e5500d0734e55499e4f"), "cantidad": 2, "calificacion": 5}], "atendidoPor": ObjectId("67432fd900d0734e55499e5d") },
    { "cliente_id": ObjectId("67432f4500d0734e55499e52"), "fecha": ISODate("2024-10-23T11:33:45Z"), "productos": [{"producto_id": ObjectId("67432e5500d0734e55499e44"), "cantidad": 15, "calificacion": 10}, {"producto_id": ObjectId("67432e5500d0734e55499e4f"), "cantidad": 5, "calificacion": 7}], "atendidoPor": ObjectId("67432fd900d0734e55499e5e") },
    { "cliente_id": ObjectId("67432f4500d0734e55499e53"), "fecha": ISODate("2024-11-22T15:22:55Z"), "productos": [{"producto_id": ObjectId("67432e5500d0734e55499e46"), "cantidad": 10, "calificacion": 10}, {"producto_id": ObjectId("67432e5500d0734e55499e47"), "cantidad": 11, "calificacion": 10}], "atendidoPor": ObjectId("67432fd900d0734e55499e5c") },
    { "cliente_id": ObjectId("67432f4500d0734e55499e54"), "fecha": ISODate("2024-11-01T17:12:00Z"), "productos": [{"producto_id": ObjectId("67432e5500d0734e55499e4c"), "cantidad": 8, "calificacion": 9}, {"producto_id": ObjectId("67432e5500d0734e55499e45"), "cantidad": 12, "calificacion": 10}], "atendidoPor": ObjectId("67432fd900d0734e55499e5f") },
    { "cliente_id": ObjectId("67432f4500d0734e55499e55"), "fecha": ISODate("2024-09-02T10:09:04Z"), "productos": [{"producto_id": ObjectId("67432e5500d0734e55499e46"), "cantidad": 12, "calificacion": 8}, {"producto_id": ObjectId("67432e5500d0734e55499e48"), "cantidad": 17, "calificacion": 9}], "atendidoPor": ObjectId("67432fd900d0734e55499e60") },
    { "cliente_id": ObjectId("67432f4500d0734e55499e56"), "fecha": ISODate("2024-08-05T08:06:15Z"), "productos": [{"producto_id": ObjectId("67432e5500d0734e55499e4c"), "cantidad": 100, "calificacion": 6}, {"producto_id": ObjectId("67432e5500d0734e55499e48"), "cantidad": 2, "calificacion": 3}], "atendidoPor": ObjectId("67432fd900d0734e55499e62") },
    { "cliente_id": ObjectId("67432f4500d0734e55499e53"), "fecha": ISODate("2024-08-09T12:02:12Z"), "productos": [{"producto_id": ObjectId("67432e5500d0734e55499e4b"), "cantidad": 7, "calificacion": 7}, {"producto_id": ObjectId("67432e5500d0734e55499e49"), "cantidad": 7, "calificacion": 1}], "atendidoPor": ObjectId("67432fd900d0734e55499e64") },
    { "cliente_id": ObjectId("67432f4500d0734e55499e57"), "fecha": ISODate("2024-04-15T11:01:14Z"), "productos": [{"producto_id": ObjectId("67432e5500d0734e55499e46"), "cantidad": 6, "calificacion": 7}, {"producto_id": ObjectId("67432e5500d0734e55499e49"), "cantidad": 21, "calificacion": 6}], "atendidoPor": ObjectId("67432fd900d0734e55499e64") },
    { "cliente_id": ObjectId("67432f4500d0734e55499e5a"), "fecha": ISODate("2024-03-16T17:50:15Z"), "productos": [{"producto_id": ObjectId("67432e5500d0734e55499e4c"), "cantidad": 22, "calificacion": 10}, {"producto_id": ObjectId("67432e5500d0734e55499e47"), "cantidad": 7, "calificacion": 6}], "atendidoPor": ObjectId("67432fd900d0734e55499e65") },
    { "cliente_id": ObjectId("67432f4500d0734e55499e5b"), "fecha": ISODate("2024-06-17T18:23:18Z"), "productos": [{"producto_id": ObjectId("67432e5500d0734e55499e4b"), "cantidad": 14, "calificacion": 2}, {"producto_id": ObjectId("67432e5500d0734e55499e47"), "cantidad": 8, "calificacion": 7}], "atendidoPor": ObjectId("67432fd900d0734e55499e5d") },
    { "cliente_id": ObjectId("67432f4500d0734e55499e55"), "fecha": ISODate("2024-07-18T21:27:33Z"), "productos": [{"producto_id": ObjectId("67432e5500d0734e55499e45"), "cantidad": 7, "calificacion": 4}, {"producto_id": ObjectId("67432e5500d0734e55499e4b"), "cantidad": 10, "calificacion": 3}], "atendidoPor": ObjectId("67432fd900d0734e55499e63") }
])

--HACEMOS LAS CONSULTAS--
1. Encuentra el producto más vendido en la tienda.
db.pedido.aggregate([
    { $unwind: "$productos" }, // Descompone el array de productos
    {
        $group: {
            _id: "$productos.producto_id", // Agrupamos por el id del producto
            total: { $sum: "$productos.cantidad" } // Sumamos la cantidad vendida de cada producto
        }
    },
    { $sort: { total: -1 } }, // Ordenamos los resultados por la cantidad total vendida (en orden descendente)
    { $limit: 1 }, // Tomamos solo el producto más vendido
    {
        $lookup: {
            from: "producto", // Buscamos la colección "producto"
            localField: "_id", // Enlazamos el campo "_id" del grupo con el campo "producto_id"
            foreignField: "_id", // En la colección de productos, buscamos por el campo "_id"
            as: "producto" // Lo almacenamos en un array llamado "producto"
        }
    },
    {
        $project: {
            _id: 0, // No mostramos el campo "_id"
            producto: { $arrayElemAt: ["$producto.nombre", 0] }, // Accedemos al primer elemento del array "producto"
            total: 1 // Mostramos la cantidad total vendida
        }
    }
]);

2. Identifica a los clientes que han realizado más de 3 pedidos en el último mes.
db.pedido.aggregate([
    // Primer paso: Filtrar los documentos para que solo se incluyan los pedidos 
    // realizados desde el 1 de noviembre de 2024 en adelante.
    {
        $match: { 
            fecha: { $gte: ISODate("2024-11-01T00:00:00Z") }  // Filtra por la fecha.
        }
    },
    
    // Segundo paso: Agrupar los documentos por el campo 'cliente_id'. 
    // Se cuenta la cantidad de pedidos por cada cliente.
    {
        $group: {
            _id: "$cliente_id",   // Agrupar por el campo cliente_id.
            totalPedidos: { $sum: 1 }  // Cuenta el número de pedidos por cliente.
        }
    },

    // Tercer paso: Filtrar los grupos (clientes) que tengan más de 3 pedidos.
    // Esto asegura que solo se devuelvan los clientes con más de 3 pedidos.
    {
        $match: { 
            totalPedidos: { $gt: 3 }  // Filtra los grupos con más de 3 pedidos.
        }
    },

    // Cuarto paso: Proyectar el resultado final, eliminando el campo _id 
    // y renombrando el campo 'cliente' con el valor de _id (que es cliente_id).
    {
        $project: {
            _id: 0,  // Elimina el campo _id.
            cliente: "$_id",  // Renombra _id a cliente.
            totalPedidos: 1  // Incluye el campo totalPedidos.
        }
    }
])

3. Calcula la ganancia total por empleado en los últimos 6 meses.
db.pedido.aggregate([
    // Fase 1: Filtrar los pedidos a partir de mayo de 2024
    {
        $match: {
            fecha: { $gte: ISODate("2024-05-01T00:00:00Z")} // Se filtran solo los pedidos cuya fecha es mayor o igual a mayo 2024
        }
    },

    // Fase 2: Deshacer los productos del pedido (unwind)
    {$unwind: "$productos"}, // Esto descompone los productos en cada documento para que cada producto del pedido tenga un documento separado
    
    // Fase 3: Unir con la colección 'producto' para obtener detalles del producto
    {
        $lookup: {
            from: "producto", // Realizamos un lookup en la colección 'producto'
            localField: "productos.producto_id", // Usamos el campo 'producto_id' del array 'productos' del pedido
            foreignField: "_id", // Buscamos que coincida con el campo '_id' de los productos
            as: "producto" // Los resultados del lookup se almacenan en un array llamado 'producto'
        }
    },
    
    // Fase 4: Agrupar los resultados por el empleado que atendió el pedido y calcular la ganancia
    {
        $group: {
            _id: "$atendidoPor", // Agrupamos por el ID del empleado que atendió el pedido
            total: {
                $sum: { 
                    // Para cada producto, multiplicamos la cantidad por el precio y luego sumamos
                    $multiply: [ 
                        "$productos.cantidad", // Cantidad del producto
                        { $first: "$producto.precio" } // Obtenemos el primer precio del producto (ya que se unió un array de productos)
                    ]
                }
            }
        }
    },

    // Fase 5: Unir con la colección 'empleado' para obtener los detalles del empleado
    {
        $lookup: {
            from: "empleado", // Realizamos un lookup en la colección 'empleado'
            localField: "_id", // Usamos el campo '_id' del grupo anterior (que corresponde al ID del empleado)
            foreignField: "_id", // Buscamos que coincida con el campo '_id' de los empleados
            as: "empleado" // Los detalles del empleado se almacenan en el array 'empleado'
        }
    },
    
    // Fase 6: Proyectar los resultados, mostrando el nombre del empleado y la ganancia total
    {
        $project: {
            _id: 0, // No mostramos el campo _id
            empleado: { $first: "$empleado.nombre" }, // Mostramos el nombre del empleado (solo el primer valor del array 'empleado')
            total: 1 // Mostramos la ganancia total calculada
        }
    }
])

4. Encuentra el promedio de precios de productos por categoría.
db.producto.aggregate([
    // Fase 1: Agrupar por categoría y calcular el promedio de precio
    {
        $group: {
            _id: "$categoria", // Agrupamos por categoría
            promedioPrecio: { $avg: "$precio" } // Calculamos el promedio de precios para cada categoría
        }
    },

    // Fase 2: Proyección para dar formato al resultado
    {
        $project: {
            _id: 0, // No mostramos el campo _id
            categoria: "$_id", // Mostramos la categoría como un campo 'categoria'
            promedioPrecio: 1 // Mostramos el promedio de precio
        }
    }
])

5. Agrupa los productos por proveedor y muestra el recuento de productos
por proveedor.
db.producto.aggregate([
    // Fase 1: Agrupar por proveedor y contar los productos
    {
        $group: {
            _id: "$proveedorId", // Agrupamos por el campo proveedorId
            totalProductos: { $sum: 1 } // Contamos el número de productos por proveedor
        }
    },

    // Fase 2: Unir con la colección 'proveedor' para obtener el nombre del proveedor
    {
        $lookup: {
            from: "proveedor", // Nombre de la colección con los proveedores
            localField: "_id", // Usamos el _id de la agrupación, que es el proveedorId
            foreignField: "_id", // Lo comparamos con el campo _id de la colección proveedor
            as: "proveedor" // Alias para los resultados de la unión
        }
    },

    // Fase 3: Proyección para dar formato al resultado
    {
        $project: {
            _id: 0, // Eliminamos el campo _id de la salida
            proveedor: { $first: "$proveedor.nombre" }, // Extraemos el nombre del proveedor
            totalProductos: 1 // Mostramos el total de productos por proveedor
        }
    }
])

6. Encuentra los productos que han estado fuera de stock por más de 30 días.
db.producto.aggregate([
    // Fase 1: Filtrar los productos que tienen stock 0 o menor
    {
        $match: {
            stock: { $lte: 0 } // Filtramos los productos con stock igual o menor a 0
        }
    },

    // Fase 2: Filtrar aquellos productos que han estado fuera de stock por más de 30 días
    {
        $match: {
            ultimaActualizacion: {
                $lte: new Date(new Date() - 30 * 24 * 60 * 60 * 1000) // Compara la fecha de la última actualización con la fecha de 30 días atrás
            }
        }
    },

    // Fase 3: Proyección para mostrar solo los campos necesarios
    {
        $project: {
            nombre: 1, // Mostrar el nombre del producto
            stock: 1, // Mostrar el stock (que debe ser 0 o menor)
            ultimaActualizacion: 1 // Mostrar la fecha de última actualización
        }
    }
])

7. Identica a los clientes que gastaron más de un cierto monto en pedidos el
último trimestre.
db.pedido.aggregate([
    {// Fase 1: Filtrar los pedidos del último trimestre
        $match: {
            fecha: { $gte: ISODate("2024-10-01T00:00:00Z") }
        }
    },// Fase 2: Desenrollar los productos de cada pedido
    {$unwind: "$productos"},
    {// Fase 3: Hacer un lookup para obtener el precio del producto
        $lookup: {
            from: "producto", 
            localField: "productos.producto_id", 
            foreignField: "_id", 
            as: "producto"
        }
    },
    { // Fase 4: Agrupar por cliente y sumar el total de los productos en cada pedido
        $group: {
            _id: "$cliente_id", 
            total: { 
                $sum: {
                    $multiply: ["$productos.cantidad", {$first: "$producto.precio"}]
                }
            }
        }
    },
    {// Fase 5: Filtrar clientes cuyo gasto total es mayor que un monto especificado
        $match: { total: { $gt: 500 }}
    },
    {// Fase 6: Lookup para obtener el nombre del cliente (suponiendo que hay una colección 'cliente')
        $lookup: {
            from: "cliente", 
            localField: "_id",  // usamos id de cliente
            foreignField: "_id", 
            as: "cliente"
        }
    },
    { // Fase 7: Proyección de los resultados finales
        $project: {
            _id: 0, 
            cliente: {$first: "$cliente.nombre"},  // mostrar el nombre del cliente
            total: 1 // muestra el total gastado
        }
    }
])
8. Encuentra los productos más populares basados en las calicaciones de los
clientes.
db.pedido.aggregate([
    // Deshacer el array de productos en los pedidos
    { $unwind: "$productos" },
    
    // Agrupar por producto_id y calcular el promedio de las calificaciones
    {
        $group: {
            _id: "$productos.producto_id", 
            avgCalificacion: { $avg: "$productos.calificacion" },
            nombre: { $first: "$productos.producto_id" } // Obtener el nombre del producto
        }
    },
    
    // Buscar información detallada del producto en la colección "producto"
    {
        $lookup: {
            from: "producto", 
            localField: "_id", 
            foreignField: "_id", 
            as: "producto"
        }
    },
    
    // Deshacer el array de "producto" para obtener los detalles
    { $unwind: "$producto" },
    
    // Ordenar los productos por el promedio de calificación en orden descendente
    { $sort: { avgCalificacion: -1 } },

    // Limitar el resultado a los productos más populares
    { $project: { _id: 0, nombre: "$producto.nombre", avgCalificacion: 1 } }
]);

9. Realiza una agregación que muestre el salario promedio de los empleados
por departamento.
db.empleado.aggregate([
    // Paso 1: Agrupar a los empleados por departamento
    {
        $group: {
            _id: "$departamento",  // Agrupar por el campo 'departamento'
            salarioPromedio: { $avg: "$salario" }  // Calcular el salario promedio de cada grupo de empleados
        }
    },
    // Paso 2: Formatear la salida
    {
        $project: {
            _id: 0,  // Eliminar el campo '_id' de la salida
            departamento: "$_id",  // Renombrar el campo '_id' a 'departamento'
            salarioPromedio: 1  // Incluir el campo 'salarioPromedio' en la salida
        }
    }
]);



-- Crea un índice simple en la colección "productos" para acelerar las búsquedas por nombre del producto.
db.productos.createIndex({ "nombre": 1 });
-- Implementa un índice compuesto en la colección "pedidos" que incluya el cliente y la fecha del pedido.
db.pedidos.createIndex({ "cliente_id": 1, "fecha": 1 });
-- Crea un índice de texto en la colección "productos" para habilitar búsquedas de texto completo en la descripción de los productos.
db.productos.createIndex({ "descripcion": "text" });

-- Para buscar algo usando el index (?)
--db.producto.find({ $text: { $search: "algodon" } });



----------------
--Busca los productos con un stock menos a 20--
db.producto.find(
    { stock: { $lt: 20 } } // Condición: stock menor a 20
);

db.cliente.deleteOne({ correo: "juan@hotmail.com" });

db.empleado.deleteMany({ departamento: "Ventas" });

db.producto.updateOne(
    { nombre: "Camiseta" },
    { $set: { precio: 25.99 } }
);

