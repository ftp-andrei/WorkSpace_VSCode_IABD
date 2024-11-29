1. Encuentra documentos con un campo mayor que el promedio de otro conjunto
db.products.aggregate([
  {
    $group: {
      _id: null,
      averagePrice: { $avg: "$price" }
    }
  },
  {
    $lookup: {
      from: "products",
      pipeline: [
        { $match: { $expr: { $gt: ["$price", "$$averagePrice"] } } }
      ],
      as: "expensiveProducts"
    }
  }
]);


2. Listar clientes con más pedidos que el promedio de todos los clientes
db.orders.aggregate([
  {
    $group: {
      _id: null,
      avgOrders: { $avg: "$order_count" }
    }
  },
  {
    $lookup: {
      from: "customers",
      pipeline: [
        { $match: { $expr: { $gt: ["$orders", "$$avgOrders"] } } }
      ],
      as: "frequentCustomers"
    }
  }
]);


3. Busca tiendas que nunca cumplieron sus objetivos de ventas
db.stores.find({ $expr: { $lt: ["$sales", "$target_sales"] } });


4. Encuentra los pedidos de un cliente y sus detalles
db.orders.aggregate([
  {
    $lookup: {
      from: "customers",
      localField: "customer_id",
      foreignField: "customer_id",
      as: "customerDetails"
    }
  },
  { $unwind: "$customerDetails" }
]);


5. Contar los productos vendidos por categoría
db.sales.aggregate([
  {
    $group: {
      _id: "$category",
      totalSold: { $sum: "$quantity" }
    }
  }
]);

6. Encuentra películas con un promedio de calificación superior a 4.5
db.movies.aggregate([
  {
    $project: {
      title: 1,
      avgRating: { $avg: "$ratings" }
    }
  },
  { $match: { avgRating: { $gt: 4.5 } } }
]);


7. Actualiza un campo basado en condiciones
db.employees.updateMany(
  { salary: { $lt: 50000 } },
  { $set: { role: "Junior Developer" } }
);


8. Filtrar documentos que contengan al menos un elemento específico en un array
db.students.find({ subjects: { $in: ["Math"] } });


9. Documentos donde un campo embebido cumple una condición
db.orders.find({ "customer.country": "USA" });


10. Encuentra productos cuyo precio sea mayor que cualquier producto en otra colección
db.products.aggregate([
  {
    $lookup: {
      from: "competitorProducts",
      as: "competitors",
      pipeline: [
        { $project: { _id: 0, maxPrice: { $max: "$price" } } }
      ]
    }
  },
  { $match: { price: { $gt: "$competitors.maxPrice" } } }
]);
