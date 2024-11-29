MongoDB
1. Consulta de Agregación en MongoDB

Pregunta: Supón que tienes una colección de libros con un campo reviews que contiene un arreglo de objetos con las calificaciones. Escribe una consulta de agregación que calcule la puntuación media de cada libro basado en las calificaciones de las reseñas.
-- 
db.book.aggregate([
  {
    $unwind: "$reviews"  // Desenrollar las reseñas del libro
  },
  {
    $group: {
      _id: "$_id",  // Agrupar por el ID del libro
      avgRating: { $avg: "$reviews.rating" }  // Calcular la puntuación media
    }
  }
])
2. Encontrar libros con reseñas de puntuación mayor a 4

Pregunta: Escribe una consulta que devuelva todos los libros que tengan al menos una reseña con una puntuación mayor a 4.
-- 
db.book.find({
  "reviews.rating": { $gt: 4 }
})
3. Insertar un nuevo libro con reseñas

Pregunta: Escribe una consulta para insertar un nuevo libro en la colección book con un título, un autor y una reseña con puntuación 5.
-- 
db.book.insertOne({
  title: "Nuevo Libro",
  author: "Autor Desconocido",
  reviews: [
    { user: "Usuario1", rating: 5, comment: "Excelente libro!" }
  ]
})
1. Consulta básica con JOIN

Pregunta: Tienes dos tablas: Books (book_id, title) y Reviews (review_id, book_id, rating, comment). Escribe una consulta que devuelva el título del libro y su calificación promedio.
-- 
SELECT b.title, AVG(r.rating) AS average_rating
FROM Books b
JOIN Reviews r ON b.book_id = r.book_id
GROUP BY b.title;
2. Filtrar los libros con calificación mayor a 4

Pregunta: Escribe una consulta que devuelva los títulos de los libros con una calificación promedio superior a 4.
-- 
SELECT b.title
FROM Books b
JOIN Reviews r ON b.book_id = r.book_id
GROUP BY b.title
HAVING AVG(r.rating) > 4;
3. Subconsulta para encontrar los libros más populares

Pregunta: Escribe una consulta que devuelva los títulos de los libros con el mayor número de reseñas.
-- 
SELECT b.title
FROM Books b
WHERE b.book_id IN (
  SELECT r.book_id
  FROM Reviews r
  GROUP BY r.book_id
  ORDER BY COUNT(r.review_id) DESC
  LIMIT 1
);
Neo4j )
1. Crear nodos y relaciones entre ellos

-- Pregunta: Escribe una consulta para crear nodos de tipo User y Book, y una relación de tipo REVIEWS entre un usuario y un libro.

CREATE (u:User {name: 'Juan'})
CREATE (b:Book {title: 'Graph Theory'})
CREATE (u)-[:REVIEWS {rating: 5, comment: 'Excellent book!'}]->(b)
2. Encontrar el camino más corto entre dos nodos

-- Pregunta: Escribe una consulta para encontrar el camino más corto entre un nodo de tipo User con nombre 'Juan' y un nodo de tipo Book con título 'Graph Theory', basándote en las relaciones de tipo REVIEWS.

MATCH (u:User {name: 'Juan'}), (b:Book {title: 'Graph Theory'})
MATCH p = shortestPath((u)-[:REVIEWS*]-(b))
RETURN p;
3. Actualizar las calificaciones de un libro

-- Pregunta: Escribe una consulta para actualizar la calificación de la reseña de un libro específico, donde el usuario 'Juan' tiene una reseña del libro 'Graph Theory'.

MATCH (u:User {name: 'Juan'})-[:REVIEWS]->(b:Book {title: 'Graph Theory'})
SET u.rating = 4  // Cambiar la calificación a 4
4. Relaciones entre nodos de tipo User y Business

-- Pregunta: Escribe una consulta para crear una relación de tipo LIKES entre un nodo User y un nodo Business.

MATCH (u:User {id: 'user1'}), (b:Business {id: 'business1'})
CREATE (u)-[:LIKES]->(b)
5. Encontrar la puntuación media de los libros

-- Pregunta: Escribe una consulta para calcular la puntuación media de todos los libros que tienen reseñas.

MATCH (b:Book)<-[:REVIEWS]-(u:User)
RETURN b.title, AVG(u.rating) AS average_rating;
Ejercicios adicionales de lógica
1. Creación de índices y optimización de consultas en Neo4j

-- Pregunta: Explica cómo crear un índice en Neo4j para la propiedad id de los nodos User y Business y cómo eso afectaría a las consultas.

CREATE INDEX FOR (u:User) ON (u.id);
CREATE INDEX FOR (b:Business) ON (b.id);




Operadores de consulta avanzados

Pregunta: ¿Cómo utilizarías los operadores $in y $nin en MongoDB para obtener todos los libros cuyo author esté en una lista de autores y que no tengan una calificación menor a 3?
-- 
db.books.find({
  author: { $in: ["Autor1", "Autor2", "Autor3"] },
  "reviews.rating": { $nin: [1, 2] }
});
2. Actualización de documentos

Pregunta: Escribe una consulta para actualizar todos los documentos de la colección book y agregar un campo genre con el valor 'Fiction' para todos los libros que no tengan este campo.
-- 
db.book.updateMany(
  { genre: { $exists: false } },
  { $set: { genre: 'Fiction' } }
);
3. Eliminar documentos

Pregunta: Escribe una consulta para eliminar todos los documentos de la colección book donde la calificación promedio en las reseñas sea inferior a 3.
-- 
db.book.deleteMany({
  "reviews.rating": { $lt: 3 }
});
4. Operadores de agregación

Pregunta: Supón que tienes una colección sales con un campo price. ¿Cómo escribirías una consulta de agregación para encontrar el precio promedio de todos los productos vendidos?
-- 
db.sales.aggregate([
  {
    $group: {
      _id: null,
      averagePrice: { $avg: "$price" }
    }
  }
]);
5. Subconsultas en MongoDB

Pregunta: ¿Cómo usarías una subconsulta para encontrar todos los usuarios que han reseñado un libro con una calificación superior a 4?
-- 
db.users.find({
  "reviews.book": { $in: db.books.find({ "reviews.rating": { $gt: 4 } }).map(book => book._id) }
});
1. Consulta con JOIN y condiciones

Pregunta: Tienes las tablas Employee (employee_id, name, department_id) y Department (department_id, department_name). Escribe una consulta para obtener el nombre del empleado y su departamento.
-- 
SELECT e.name, d.department_name
FROM Employee e
JOIN Department d ON e.department_id = d.department_id;
2. Uso de GROUP BY y HAVING

Pregunta: Escribe una consulta que devuelva los departamentos con más de 5 empleados. Debes usar las tablas Employee (employee_id, name, department_id) y Department (department_id, department_name).
-- 
SELECT d.department_name, COUNT(e.employee_id) AS num_employees
FROM Employee e
JOIN Department d ON e.department_id = d.department_id
GROUP BY d.department_name
HAVING COUNT(e.employee_id) > 5;
3. Subconsulta con EXISTS

Pregunta: Escribe una consulta que devuelva los empleados que tienen al menos un salario superior a $50,000.
-- 
SELECT name
FROM Employee e
WHERE EXISTS (
  SELECT 1
  FROM Salary s
  WHERE s.employee_id = e.employee_id AND s.amount > 50000
);
4. Uso de CASE

Pregunta: Supón que tienes la tabla Orders (order_id, order_date, total_amount). Escribe una consulta para obtener el total de ventas por mes y clasificar el mes como "Alto", "Medio" o "Bajo" según el total de ventas.
-- 
SELECT
  EXTRACT(MONTH FROM order_date) AS month,
  SUM(total_amount) AS total_sales,
  CASE
    WHEN SUM(total_amount) > 10000 THEN 'Alto'
    WHEN SUM(total_amount) BETWEEN 5000 AND 10000 THEN 'Medio'
    ELSE 'Bajo'
  END AS sales_category
FROM Orders
GROUP BY EXTRACT(MONTH FROM order_date);
5. INNER JOIN y LEFT JOIN

Pregunta: ¿Cuál es la diferencia entre un INNER JOIN y un LEFT JOIN? Proporciona un ejemplo de consulta para cada uno.

INNER JOIN: Devuelve solo las filas que tienen una coincidencia en ambas tablas.
LEFT JOIN: Devuelve todas las filas de la tabla izquierda y las filas coincidentes de la tabla derecha, o NULL si no hay coincidencia.
Ejemplo de INNER JOIN:
-- 
SELECT e.name, d.department_name
FROM Employee e
INNER JOIN Department d ON e.department_id = d.department_id;
Ejemplo de LEFT JOIN:
-- 
SELECT e.name, d.department_name
FROM Employee e
LEFT JOIN Department d ON e.department_id = d.department_id;
Neo4j )
1. Crear nodos y relaciones

-- Pregunta: Escribe una consulta para crear dos nodos de tipo Person y una relación FRIEND entre ellos.

CREATE (p1:Person {name: 'Alice'})
CREATE (p2:Person {name: 'Bob'})
CREATE (p1)-[:FRIEND]->(p2)
2. Buscar nodos por propiedad

-- Pregunta: Escribe una consulta para encontrar todos los libros con un rating superior a 4.

MATCH (b:Book)
WHERE b.rating > 4
RETURN b.title
3. Contar nodos de un tipo

-- Pregunta: Escribe una consulta para contar cuántos usuarios (User) han dejado reseñas.

MATCH (u:User)-[:REVIEWS]->(b:Book)
RETURN COUNT(u)
4. Actualización de propiedades en nodos

-- Pregunta: Escribe una consulta para actualizar la propiedad rating de la reseña hecha por el usuario 'Juan' para el libro 'Graph Theory'.

MATCH (u:User {name: 'Juan'})-[:REVIEWS]->(b:Book {title: 'Graph Theory'})
SET u.rating = 4
5. Relación entre nodos de diferentes tipos

-- Pregunta: Escribe una consulta para encontrar todos los libros que han sido reseñados por un usuario con el nombre 'Juan'.

MATCH (u:User {name: 'Juan'})-[:REVIEWS]->(b:Book)
RETURN b.title
6. Eliminar nodos y relaciones

-- Pregunta: Escribe una consulta para eliminar todos los nodos de tipo User que no tienen reseñas asociadas.

MATCH (u:User)
WHERE NOT (u)-[:REVIEWS]->()
DELETE u
7. Crear una relación con múltiples propiedades

-- Pregunta: Escribe una consulta para crear una relación entre un User y un Book con una propiedad adicional date que indique cuándo fue la reseña.

MATCH (u:User {name: 'Juan'}), (b:Book {title: 'Graph Theory'})
CREATE (u)-[:REVIEWS {rating: 5, date: '2024-11-29'}]->(b)



MongoDB
1. Operaciones de actualización

Pregunta: ¿Cómo actualizarías el campo address de un documento de la colección customers para un cliente específico identificado por su customer_id? ¿Y cómo hacerlo para actualizar solo un campo dentro de un documento anidado?
--
js
db.customers.updateOne(
  { customer_id: 12345 },
  { $set: { "address.city": "New York" } }
);
2. Operaciones de agregación

Pregunta: ¿Cómo escribirías una consulta de agregación en MongoDB para encontrar el total de ventas por año, usando un campo sale_date de tipo fecha en la colección sales?
--
js
db.sales.aggregate([
  { $group: { _id: { $year: "$sale_date" }, total_sales: { $sum: "$amount" } } }
]);
3. Filtrar con regex

Pregunta: ¿Cómo usarías una expresión regular en MongoDB para encontrar todos los usuarios cuyo nombre comienza con "J"?
--
js
db.users.find({ name: { $regex: "^J" } });
4. Proyecciones en MongoDB

Pregunta: Escribe una consulta para obtener solo el campo name y email de todos los documentos en la colección customers.
--
js
db.customers.find({}, { name: 1, email: 1 });
5. Operación lookup

Pregunta: ¿Cómo realizarías una operación de lookup para combinar los datos de las colecciones orders y customers, donde la clave de unión es customer_id?
--
js
db.orders.aggregate([
  {
    $lookup: {
      from: "customers",
      localField: "customer_id",
      foreignField: "customer_id",
      as: "customer_info"
    }
  }
]);
1. Uso de DISTINCT

Pregunta: ¿Cómo escribirías una consulta para obtener una lista de departamentos únicos de la tabla employees?
--
SELECT DISTINCT department FROM employees;
2. Subconsultas con IN

Pregunta: Escribe una consulta para obtener los empleados que trabajen en los departamentos que tienen más de 10 empleados.
--
SELECT e.name
FROM Employee e
WHERE e.department_id IN (
  SELECT d.department_id
  FROM Department d
  JOIN Employee e ON e.department_id = d.department_id
  GROUP BY d.department_id
  HAVING COUNT(e.employee_id) > 10
);
3. Joins entre múltiples tablas

Pregunta: Tienes las tablas students (id, name) y courses (course_id, course_name) y una tabla de relación enrollments (student_id, course_id). ¿Cómo escribirías una consulta para encontrar los estudiantes que están inscritos en el curso 'Mathematics'?
--
SELECT s.name
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.course_id
WHERE c.course_name = 'Mathematics';
4. Uso de funciones agregadas

Pregunta: Escribe una consulta que calcule la cantidad total de productos vendidos y el ingreso total de la tabla sales (con campos product_id, quantity, price).
--
SELECT SUM(quantity) AS total_sold, SUM(quantity * price) AS total_income
FROM sales;
5. Operadores BETWEEN y LIKE

Pregunta: Escribe una consulta para obtener todos los productos cuyo precio esté entre 50 y 150 y cuyo nombre contenga la palabra "Electro".
--
SELECT * FROM products
WHERE price BETWEEN 50 AND 150
AND product_name LIKE '%Electro%';
Neo4j )
1. Búsqueda de nodos con propiedades específicas

--Pregunta: Escribe una consulta para encontrar todos los usuarios que han dejado una reseña para un libro titulado "Graph Theory".

MATCH (u:User)-[:REVIEWS]->(b:Book {title: 'Graph Theory'})
RETURN u.name;
2. Crear nodos y relaciones con propiedades

--Pregunta: Escribe una consulta para crear un nuevo nodo Author con propiedades name y birthdate, y una relación WROTE entre el autor y un libro llamado 'Introduction to Graph Theory'.

CREATE (a:Author {name: 'John Doe', birthdate: '1975-01-01'})
CREATE (b:Book {title: 'Introduction to Graph Theory'})
CREATE (a)-[:WROTE]->(b)
3. Encontrar caminos más cortos entre nodos

--Pregunta: Escribe una consulta para encontrar el camino más corto entre dos nodos de tipo Person por las relaciones FRIEND.

MATCH (p1:Person {name: 'Alice'}), (p2:Person {name: 'Bob'}), 
      p = shortestPath((p1)-[:FRIEND*]-(p2))
RETURN p;
4. Eliminar nodos y relaciones

--Pregunta: Escribe una consulta para eliminar una relación FRIEND entre dos personas, Alice y Bob.

MATCH (p1:Person {name: 'Alice'})-[r:FRIEND]->(p2:Person {name: 'Bob'})
DELETE r;
5. Búsqueda de nodos con relaciones y propiedades

--Pregunta: Escribe una consulta para encontrar todos los usuarios que han dejado una reseña con calificación superior a 4 para un libro titulado "Machine Learning Basics".

MATCH (u:User)-[r:REVIEWS]->(b:Book {title: 'Machine Learning Basics'})
WHERE r.rating > 4
RETURN u.name;

