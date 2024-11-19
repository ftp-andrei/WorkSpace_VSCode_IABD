docker exec -it MongoContainerBDA bin/bash

mongosh -u mongoadmin -p secret --authenticationDatabase admin

use LiteraWorld


-- **  Ejercicios ** --
Crea las colecciones y añade al menos 4 documentos por colección

db.createCollection("Libros")
db.createCollection("Editorial")
db.createCollection("Autor")
db.createCollection("Clientes")

db.Libros.insertMany( [
      { idLibro: 1, titulo: "asesinato en el orient express", precio: 20, genero: "terror", },
      { idLibro: 2, titulo: "el ciclo del eterno emperador", precio: 55, genero: "fantasia", },
      { idLibro: 3, titulo: "arthur lupin", precio: 30, genero: "terror", },
      { idLibro: 4, titulo: "percy jackson el mar de monstruos", precio: 30, genero: "fantasia", }
])

db.Editorial.insertMany( [
      { idEditorial: 1, nombre: "Circulo de lectores", ano_fundacion:1888, sede:"Madrid", libros: {idLibro:1,idLibro:2} },
      { idEditorial: 2, nombre: "Planeta", ano_fundacion:1950, sede:"Copenhage",libros: {idLibro:3} },
      { idEditorial: 3, nombre: "Nova",ano_fundacion:1999,sede:"Berlín", libros: {idLibro:3,idLibro:4} }
])

db.Autor.insertMany( [
      { idAutor: 1, nombre: "Agatha Christie", nacionalidad: "Britanica", librosEscritos:{idLibro:1} },
      { idAutor: 2, nombre: "J.R.R. Tolkien", nacionalidad: "Britanica", librosEscritos:{idLibro:2} },
      { idAutor: 3, nombre: "J.K. Rowling", nacionalidad: "Britanica", librosEscritos:{idLibro:3} },
      { idAutor: 4, nombre: "Rick Riordan", nacionalidad: "Britanica", librosEscritos:{idLibro:1,idLibro:4} }
])

db.Clientes.insertMany( [
      { idCliente:1,nombre: "Juan", email: "juan@example.com", direccion: "Calle Principal 123", reseña: "Excelente libro", idLibro: 1 },
      { idCliente:2, nombre: "María", email: "maria@example.com", direccion: "Avenida Central 456", reseña: "Buen libro", idLibro: 2 },
      { idCliente:3, nombre: "Pedro", email: "pedro@example.com", direccion: "Calle Secundaria 789", reseña: "Muy interesante", idLibro: 3 },
      { idCliente:4, nombre: "Ana", email: "ana@example.com", direccion: "Avenida Principal 101", reseña: "Increíble", idLibro: 4 }
])


------RAFA------------
db.authors.insertMany([
  { 
    name: "George Orwell",
    dob: ISODate("1903-06-25"),
    nationality: "British"
  },
  { 
    name: "Harper Lee",
    dob: ISODate("1926-04-28"),
    nationality: "American"
  }
]);


db.publishers.insertMany([
  {
    name: "Secker & Warburg",
    address: "London, UK",
    founded: 1935
  },
  {
    name: "J.B. Lippincott & Co.",
    address: "Philadelphia, USA",
    founded: 1836
  }
]);


db.books.insertMany([
  {
    title: "1984",
    genre: "Dystopian",
    publicationYear: 1949,
    price: 15.99,
    rating: 4.7,
    author: ObjectId('67339a0ac5077641bafe6920'),
    publisher: ObjectId('67339a0fc5077641bafe6923') 
  },
  {
    title: "Animal Farm",
    genre: "Political Satire",
    publicationYear: 1945,
    price: 9.99,
    rating: 4.6,
    author: ObjectId('67339a0ac5077641bafe6921'),
    publisher: ObjectId('67339a0fc5077641bafe6923')
  },
  {
    title: "To Kill a Mockingbird",
    genre: "Fiction",
    publicationYear: 1960,
    price: 10.99,
    rating: 4.8,
    author: ObjectId('67339a0ac5077641bafe6921'),
    publisher: ObjectId('67339a0fc5077641bafe6922')
  }	
]);


db.customers.insertMany([
  { 
    name: "Alice Johnson",
    email: "alice@example.com",
    address: "123 Maple Street, Springfield",
    reviews: [
      {
        rating: 5,
        text: "A timeless classic!",
        book: ObjectId('67339a68c5077641bafe6924')
      },
      {
        rating: 5,
        text: "A masterpiece.",
        book: ObjectId('67339a68c5077641bafe6925'),
      }
    ]
  },
  {
    name: "Bob Smith",
    email: "bob@example.com",
    address: "456 Oak Street, Springfield",
    reviews: [
      {
        rating: 4,
        text: "Thought-provoking.",
        book: ObjectId('67339a68c5077641bafe6926')
      }
    ]
  }
]);
------------------


1. Enumere todos los libros con una calificación superior a 4,5.

db.books.aggregate([
{
    $match: {
        rating: { $gt: 4.5 }
    }
}
])


-- devuelve el rating mas grande

db.books.aggregate([
{
    $sort: { rating: -1 },
    { $limit: 1 }
}
])

2. Calcular la puntuación media de cada libro.

db.customers.aggregate([
{ $unwind: "$reviews" },
{
    $group: {
        _id: "$reviews.book",
        averageRating: { $avg: "$reviews.rating" }
    }
},
{
    $lookup: {
        from: "books",
        localField: "_id",
        foreignField: "_id",
        as: "bookInfo"
    }
}, 
{ unwind: "$bookInfo" },
{
    $project: {
        _id: 0,
        title: "$bookInfo.title",
        averageRating: 1
    }
}
])

3. Encontrar el número total de libros publicados por cada editorial.
db.books.aggregate([
{
    $group: {
        _id: "$publisher",
        totalBooks: { $sum: 1 }
    }
},
{
    $lookup: {
        from: "publishers",
        localField: "_id",
        foreignField: "_id",
        as: "publisherInfo"
    }
},
{ $unwind: "$publisherInfo" },
{
    $project: {
        _id: 0,
        publisherName: "$publisherInfo.name",
        totalBooks: 1
    }
}
])
--- Lo mimso pero con el nombre de los libros (push)

db.books.aggregate([
  {
    $group: {
      _id: "$gender",
      averagePrice: { $avg: "$price" },
      libros: { $push: "$title" }
    }
  },
])

4. Mostrar el precio medio de los libros de cada género.
db.books.aggregate([
{
    $group: {
        _id: "$gender",
        averagePrice: { $avg: "$price" }
    }
}
])

5. Enumerar los autores junto con el número total de reseñas que han recibido sus
libros.
--gpt hasta fin
db.books.aggregate([
{
    $lookup: {
        from: "authors",
        localField: "author",
        foreignField: "_id",
        as: "authorInfo"
    }
},
{ $unwind: "$authorInfo" },
{
    $group: {
        _id: "$authorInfo.name",
        totalReviews: { $sum: { $size: "$reviews" } }
    }
}
])
6. Encuentre el libro mejor valorado de cada editorial.
db.books.aggregate([
{ $sort: { rating: -1 } },
{
    $group: {
        _id: "$publisher",
        topRatedBook: { $first: "$$ROOT" }
    }
},
{
    $lookup: {
        from: "publishers",
        localField: "_id",
        foreignField: "_id",
        as: "publisherInfo"
    }
},
{ $unwind: "$publisherInfo" },
{
    $project: {
        _id: 0,
        publisherName: "$publisherInfo.name",
        topRatedBook: 1
    }
}
])
7. Calcular la valoración media de los libros de cada autor.
db.books.aggregate([
{
    $lookup: {
        from: "authors",
        localField: "author",
        foreignField: "_id",
        as: "authorInfo"
    }
},
{ $unwind: "$authorInfo" },
{
    $group: {
        _id: "$authorInfo.name",
        averageRating: { $avg: "$rating" }
    }
}
])
8. Mostrar la distribución porcentual de libros por género.
db.books.aggregate([
{
    $group: {
        _id: "$gender",
        count: { $sum: 1 }
    }
},
{
    $project: {
        _id: 0,
        gender: "$_id",
        percentage: {
            $multiply: [
                { $divide: ["$count", { $sum: "$count" }] },
                100
            ]
        }
    }
}
])
9. Identificar a los clientes que han reseñado más de un libro, mostrando sus nombres y
los libros que han reseñado.
db.customers.aggregate([
{ $unwind: "$reviews" },
{
    $group: {
        _id: "$_id",
        name: { $first: "$name" },
        reviewedBooks: { $addToSet: "$reviews.book" }
    }
},
{
    $match: {
        $expr: { $gt: [{ $size: "$reviewedBooks" }, 1] }
    }
},
{
    $project: {
        _id: 0,
        name: 1,
        reviewedBooks: 1
    }
}
])
10. Para cada editorial, enumere los libros en orden descendente de puntuación,
incluyendo el número total de reseñas que ha recibido cada libro.
db.books.aggregate([
{
    $lookup: {
        from: "publishers",
        localField: "publisher",
        foreignField: "_id",
        as: "publisherInfo"
    }
},
{ $unwind: "$publisherInfo" },
{ $sort: { rating: -1 } },
{
    $group: {
        _id: "$publisherInfo.name",
        books: {
            $push: {
                title: "$title",
                rating: "$rating",
                totalReviews: { $size: "$reviews" }
            }
        }
    }
}
])