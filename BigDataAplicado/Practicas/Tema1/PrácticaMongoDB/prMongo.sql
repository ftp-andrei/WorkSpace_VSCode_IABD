use tienda

db.createCollection("producto")
db.createCollection("cliente")
db.createCollection("pedido")
db.createCollection("proveedor")


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
      { "nombre": "Camiseta 1", "precio": 19.99, "descripcion": "Es de algodon", "categoria": "Ropa de vestir", "stock": 100, "proveedorId": ObjectId() },
      { "nombre": "Pantalones Vaqueros", "precio": 30.00, "descripcion": "De buena calidad", "categoria": "Ropa de vestir", "stock": 55, "proveedorId": ObjectId()  },
      { "nombre": "Zapatillas", "precio": 99.99, "descripcion": "Made in China", "categoria": "Calzado", "stock": 10, "proveedorId": ObjectId()  },
      { "nombre": "Caramelos", "precio": 1.99, "descripcion": "Halls", "categoria": "Dulces", "stock": 14, "proveedorId": ObjectId()  },
      { "nombre": "Chicles", "precio": 0.99, "descripcion": "Trident", "categoria": "Dulces", "stock": 17, "proveedorId": ObjectId()  },
      { "nombre": "Bombones", "precio": 4.99, "descripcion": "Lindt", "categoria": "Chocolates & Surtidos", "stock": 22, "proveedorId": ObjectId()  },
      { "nombre": "Luces de navidad", "precio": 34.99, "descripcion": "Luces led 30m", "categoria": "Navidad", "stock": 25, "proveedorId": ObjectId()  },
      { "nombre": "Telefono", "precio": 499.95, "descripcion": "Xiaomi Redmi", "categoria": "Informatica", "stock": 10, "proveedorId": ObjectId()  },
      { "nombre": "Ordenador", "precio": 999.95, "descripcion": "Gama alta, 4090ti + R9 7950X", "categoria": "Informatica", "stock": 1000, "proveedorId": ObjectId()  },
      { "nombre": "Teclado", "precio": 69.98, "descripcion": "Mecanico switches red", "categoria": "Informatica", "stock": 500, "proveedorId": ObjectId()  },
      { "nombre": "Cable usb C", "precio": 6.95, "descripcion": "1,5M 30w", "categoria": "Informatica", "stock": 5000, "proveedorId": ObjectId()  },
      { "nombre": "Adornos navidad", "precio": 3.95, "descripcion": "Surtido variado adornos", "categoria": "Navidad", "stock": 40, "proveedorId": ObjectId()  },
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
    { "cliente_id": ObjectId(), "fecha": ISODate("2024-03-23T10:30:01Z"), "productos": [{"producto_id": ObjectId(), "cantidad": 4}, {"producto_id": ObjectId(), "cantidad": 1}], "total": 150, "atendidoPor": ObjectId() },
    { "cliente_id": ObjectId(), "fecha": ISODate("2024-05-11T11:31:30Z"), "productos": [{"producto_id": ObjectId(), "cantidad": 3}, {"producto_id": ObjectId(), "cantidad": 2}], "total": 7, "atendidoPor": ObjectId() },
    { "cliente_id": ObjectId(), "fecha": ISODate("2024-10-23T11:33:45Z"), "productos": [{"producto_id": ObjectId(), "cantidad": 15}, {"producto_id": ObjectId(), "cantidad": 5}], "total": 1035, "atendidoPor": ObjectId() },
    { "cliente_id": ObjectId(), "fecha": ISODate("2024-11-22T15:22:55Z"), "productos": [{"producto_id": ObjectId(), "cantidad": 10}, {"producto_id": ObjectId(), "cantidad": 11}], "total": 73, "atendidoPor": ObjectId() },
    { "cliente_id": ObjectId(), "fecha": ISODate("2024-11-01T17:12:00Z"), "productos": [{"producto_id": ObjectId(), "cantidad": 8}, {"producto_id": ObjectId(), "cantidad": 12}], "total": 150, "atendidoPor": ObjectId() },
    { "cliente_id": ObjectId(), "fecha": ISODate("2024-09-02T10:09:04Z"), "productos": [{"producto_id": ObjectId(), "cantidad": 12}, {"producto_id": ObjectId(), "cantidad": 17}], "total": 7, "atendidoPor": ObjectId() },
    { "cliente_id": ObjectId(), "fecha": ISODate("2024-08-05T08:06:15Z"), "productos": [{"producto_id": ObjectId(), "cantidad": 100}, {"producto_id": ObjectId(), "cantidad": 2}], "total": 1035, "atendidoPor": ObjectId() },
    { "cliente_id": ObjectId(), "fecha": ISODate("2024-08-09T12:02:12Z"), "productos": [{"producto_id": ObjectId(), "cantidad": 7}, {"producto_id": ObjectId(), "cantidad": 7}], "total": 73, "atendidoPor": ObjectId() },
    { "cliente_id": ObjectId(), "fecha": ISODate("2024-04-15T11:01:14Z"), "productos": [{"producto_id": ObjectId(), "cantidad": 6}, {"producto_id": ObjectId(), "cantidad": 21}], "total": 150, "atendidoPor": ObjectId() },
    { "cliente_id": ObjectId(), "fecha": ISODate("2024-03-16T17:50:15Z"), "productos": [{"producto_id": ObjectId(), "cantidad": 22}, {"producto_id": ObjectId(), "cantidad": 7}], "total": 7, "atendidoPor": ObjectId() },
    { "cliente_id": ObjectId(), "fecha": ISODate("2024-06-17T18:23:18Z"), "productos": [{"producto_id": ObjectId(), "cantidad": 14}, {"producto_id": ObjectId(), "cantidad": 8}], "total": 1035, "atendidoPor": ObjectId() },
    { "cliente_id": ObjectId(), "fecha": ISODate("2024-07-18T21:27:33Z"), "productos": [{"producto_id": ObjectId(), "cantidad": 7}, {"producto_id": ObjectId(), "cantidad": 10}], "total": 73, "atendidoPor": ObjectId() }
])


1. Encuentra el producto más vendido en la tienda.
db.pedido.aggregate([
    {$unwind: "$productos"},
    {
        $group: {
            _id: "$productos.producto_id", 
            total: { $sum: "$productos.cantidad" }
        }
    },
    {$sort: {total: -1}},
    {$limit: 1},
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
            _id: 0, 
            producto: { $first: "$producto.nombre" }, 
            total: 1
        }
    }
])
2. Identica a los clientes que han realizado más de 3 pedidos en el último
mes.
db.pedido.aggregate([
    {
        $match: { fecha: { $gte: ISODate("2024-11-01T00:00:00Z") }}
    },
    {
        $group: {
            _id: "$cliente_id", 
            total: {$sum: 1}
        }
    },
    {
        $match: { total: { $gt: 3 }}
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
            _id: 0, 
            cliente: { $first: "$cliente.nombre" }, 
            total: 1
        }
    }
])
3. Calcula la ganancia total por empleado en los últimos 6 meses.
db.pedido.aggregate([
    {
        $match: {
            fecha: { $gte: ISODate("2024-05-01T00:00:00Z")}
        }
    },
    {$unwind: "$productos"},
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
            _id: "$atendidoPor", 
            total: {
                $sum: { $multiply: [ "$productos.cantidad", { $first: "$producto.precio" }]}
            }
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
            _id: 0, 
            empleado: { $first: "$empleado.nombre" }, 
            total: 1
        }
    }
])
4. Encuentra el promedio de precios de productos por categoría.
db.producto.aggregate([
    {
        $group: {
            _id: "$categoria", 
            precio: { $avg: "$precio" }
        }
    },
    {
        $project: {
            _id: 0, 
            categoria: "$_id", 
            precio: 1
        }
    }
])
5. Agrupa los productos por proveedor y muestra el recuento de productos
por proveedor.
db.producto.aggregate([
    {
        $group: {
            _id: "$proveedorId", 
            total: { $sum: 1 }
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
            proveedor: {$first: "$proveedor.nombre"}, 
            total: 1
        }
    }
])
6. Encuentra los productos que han estado fuera de stock por más de 30 días.
db.producto.aggregate([
    { $match: { stock: 0 }},
    {
        $project: {
            nombre: 1, 
            fecha: { $subtract: [ISODate(), "$fecha"]}
        }
    },
    { $match: { fecha: { $gt: 30 }}},
    {$project: {_id: 0, nombre: 1}}
])
7. Identica a los clientes que gastaron más de un cierto monto en pedidos el
último trimestre.
db.pedido.aggregate([
    {
        $match: {
            fecha: { $gte: ISODate("2024-10-01T00:00:00Z") }
        }
    },
    {$unwind: "$productos"},
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
            _id: "$cliente_id", 
            total: { 
                $sum: {
                    $multiply: ["$productos.cantidad", {$first: "$producto.precio"}]
                }
            }
        }
    },
    {
        $match: { total: { $gt: 500 }}
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
            _id: 0, 
            cliente: {$first: "$cliente.nombre"}, 
            total: 1
        }
    }
])
8. Encuentra los productos más populares basados en las calicaciones de los
clientes.
db.pedido.aggregate([
    {$unwind: "$productos"},
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
            _id: "$productos.producto_id", 
            total: { $sum: "$productos.cantidad" }, 
            nombre: { $first: "$producto.nombre" }
        }
    },
    {$sort: {total: -1}},
    {$limit: 1},
    {$project: {_id: 0, nombre: 1, total: 1}}
])
9. Realiza una agregación que muestre el salario promedio de los empleados
por departamento.
db.empleado.aggregate([
    {
        $group: {
            _id: "$departamento", 
            salario: { $avg: "$salario" }
        }
    },
    {
        $project: {
            _id: 0, 
            departamento: "$_id", 
            salario: 1
        }
    }
])


-- Crea un índice simple en la colección "productos" para acelerar las búsquedas por nombre del producto.
db.productos.createIndex({ "nombre": 1 });
-- Implementa un índice compuesto en la colección "pedidos" que incluya el cliente y la fecha del pedido.
db.pedidos.createIndex({ "cliente_id": 1, "fecha": 1 });
-- Crea un índice de texto en la colección "productos" para habilitar búsquedas de texto completo en la descripción de los productos.
db.productos.createIndex({ "descripcion": "text" });