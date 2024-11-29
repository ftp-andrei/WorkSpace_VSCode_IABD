db.clientes.insertMany([
    {
      _id: 1,
      nombre: "Carlos Pérez",
      email: "carlos@example.com",
      direccion: {
        calle: "Calle Falsa 123",
        ciudad: "Madrid",
        pais: "España",
        codigoPostal: "28080"
      },
      telefono: ["+34 912345678", "+34 654987321"],
      fechaRegistro: new Date("2023-05-15"),
      historialCompras: [
        { productoId: 101, cantidad: 2, fecha: new Date("2023-06-10"), total: 200 },
        { productoId: 103, cantidad: 1, fecha: new Date("2023-07-12"), total: 150 }
      ]
    },
    {
      _id: 2,
      nombre: "Ana López",
      email: "ana@example.com",
      direccion: {
        calle: "Avenida del Sol 45",
        ciudad: "Sevilla",
        pais: "España",
        codigoPostal: "41001"
      },
      telefono: ["+34 687654321"],
      fechaRegistro: new Date("2023-07-25"),
      historialCompras: [
        { productoId: 102, cantidad: 3, fecha: new Date("2023-08-02"), total: 300 }
      ]
    },
    {
      _id: 3,
      nombre: "Luis Gómez",
      email: "luis@example.com",
      direccion: {
        calle: "Calle Luna 9",
        ciudad: "Valencia",
        pais: "España",
        codigoPostal: "46000"
      },
      telefono: ["+34 654321987"],
      fechaRegistro: new Date("2023-03-30"),
      historialCompras: [
        { productoId: 101, cantidad: 1, fecha: new Date("2023-04-01"), total: 100 },
        { productoId: 104, cantidad: 1, fecha: new Date("2023-07-20"), total: 50 }
      ]
    }
  ]);

  db.productos.insertMany([
    {
      _id: 101,
      nombre: "Camiseta Deportiva",
      descripcion: "Camiseta de algodón para hacer deporte.",
      precio: 100,
      categoriaId: 1,
      stock: 50
    },
    {
      _id: 102,
      nombre: "Pantalón Deportivo",
      descripcion: "Pantalón cómodo para actividades físicas.",
      precio: 120,
      categoriaId: 1,
      stock: 30
    },
    {
      _id: 103,
      nombre: "Zapatillas Running",
      descripcion: "Zapatillas ligeras para correr.",
      precio: 150,
      categoriaId: 2,
      stock: 20
    },
    {
      _id: 104,
      nombre: "Sombrero Playa",
      descripcion: "Sombrero de paja para la playa.",
      precio: 50,
      categoriaId: 3,
      stock: 100
    }
  ]);
    
  db.ordenes.insertMany([
    {
      _id: 1001,
      clienteId: 1,
      productos: [
        { productoId: 101, cantidad: 2, precioUnitario: 100 },
        { productoId: 103, cantidad: 1, precioUnitario: 150 }
      ],
      fechaOrden: new Date("2023-06-10"),
      total: 450,
      estado: "Enviado"
    },
    {
      _id: 1002,
      clienteId: 2,
      productos: [
        { productoId: 102, cantidad: 3, precioUnitario: 120 }
      ],
      fechaOrden: new Date("2023-08-02"),
      total: 360,
      estado: "Enviado"
    },
    {
      _id: 1003,
      clienteId: 3,
      productos: [
        { productoId: 101, cantidad: 1, precioUnitario: 100 },
        { productoId: 104, cantidad: 1, precioUnitario: 50 }
      ],
      fechaOrden: new Date("2023-07-20"),
      total: 150,
      estado: "Pendiente"
    }
  ]);

  db.categorias.insertMany([
    { _id: 1, nombre: "Ropa Deportiva" },
    { _id: 2, nombre: "Calzado" },
    { _id: 3, nombre: "Accesorios" }
  ]);

  Buscar un cliente por nombre
  db.clientes.find({ nombre: "Carlos Pérez" });

  Buscar productos por categoría (ejemplo: "Ropa Deportiva")
  db.productos.find({ categoriaId: 1 });
  
  Consultar órdenes de un cliente (por ejemplo, "Carlos Pérez")
  db.ordenes.find({ clienteId: 1 });

  Consultar productos que estén agotados (stock == 0)
  db.productos.find({ stock: 0 });


  Total gastado por cada cliente
  Queremos saber cuánto ha gastado cada cliente en total en la tienda. Utilizamos 
  un Aggregation Pipeline que combine los datos de la colección de clientes y las órdenes:

  db.clientes.aggregate([
    {
      $lookup: {
        from: "ordenes",
        localField: "_id",
        foreignField: "clienteId",
        as: "ordenes_cliente"
      }
    },
    {
      $unwind: "$ordenes_cliente"
    },
    {
      $group: {
        _id: "$nombre",
        totalGastado: { $sum: "$ordenes_cliente.total" }
      }
    }
  ]);
  
  Promedio de compras por cliente
  db.clientes.aggregate([
    {
      $lookup: {
        from: "ordenes",
        localField: "_id",
        foreignField: "clienteId",
        as: "ordenes_cliente"
      }
    },
    {
      $unwind: "$ordenes_cliente"
    },
    {
      $group: {
        _id: "$nombre",
        promedioGasto: { $avg: "$ordenes_cliente.total" }
      }
    }
  ]);
  
  Productos más vendidos (por cantidad)
  db.ordenes.aggregate([
    { $unwind: "$productos" },
    {
      $group: {
        _id: "$productos.productoId",
        totalVendidos: { $sum: "$productos.cantidad" }
      }
    },
    { $sort: { totalVendidos: -1 } }
  ]);

  Listado de productos con su categoría
  db.productos.aggregate([
    {
      $lookup: {
        from: "categorias",
        localField: "categoriaId",
        foreignField: "_id",
        as: "categoria"
      }
    },
    { $unwind: "$categoria" },
    {
      $project: {
        nombre: 1,
        descripcion: 1,
        precio: 1,
        categoria: "$categoria.nombre"
      }
    }
  ]);
  

