MATCH (n:Person {name: 'Anna'})-[:KNOWS]-{1,5}(friend:Person WHERE n.born < friend.born)
RETURN DISTINCT friend.name AS olderConnections

MATCH p = SHORTEST 1 (:Person {name: 'Anna'})-[:KNOWS]-+(:Person {nationality: 'Canadian'})
RETURN p

MATCH (tom:Person {name:'Tom Hanks'})-[r]->(m:Movie)
RETURN type(r) AS type, m.title AS movie

CREATE (u:Usuario {nombre "Juan", email "juan@gmail.com", eda: 30})

CREATE (charlie:Person:Actor {name: 'Charlie Sheen'}), (oliver:Person:Director {name: 'Oliver Stone'})

CREATE (charlie:Person:Actor {name: 'Charlie Sheen'})-[:ACTED_IN {role: 'Bud Fox'}]->(wallStreet:Movie {title: 'Wall Street'})<-[:DIRECTED]-(oliver:Person:Director {name: 'Oliver Stone'})

MATCH (charlie:Person {name: 'Charlie Sheen'}), (oliver:Person {name: 'Oliver Stone'})
CREATE (charlie)-[:ACTED_IN {role: 'Bud Fox'}]->(wallStreet:Movie {title: 'Wall Street'})<-[:DIRECTED]-(oliver)

CREATE p = (charlie:Person:Actor {name: 'Charlie Sheen'})-[:ACTED_IN {role: 'Bud Fox'}]->(wallStreet:Movie {title: 'Wall Street'})<-[:DIRECTED]-(oliver:Person:Director {name: 'Oliver Stone'}), (wallStreet)<-[:ACTED_IN {role: 'Gordon Gekko'}]-(michael:Person:Actor {name: 'Michael Douglas'})
RETURN length(p)

MATCH (charlie:Person {name: 'Charlie Sheen'})
CREATE (charlie:Actor)

MATCH (person:Person)
  WHERE person.name IS NOT NULL
CREATE (anotherPerson:Person {name: person.name, age: $age})

CREATE (charlie {score: oliver.score + 1}), (oliver {score: charlie.score + 1})

LOAD CSV FROM 'file:///artists.csv' AS row
MERGE (a:Artist {name: row[1], year: toInteger(row[2])})
RETURN a.name, a.year

LOAD CSV FROM 'ftp://<username>:<password>@<domain>/bands/artists.csv' AS row
MERGE (a:Artist {name: row[1], year: toInteger(row[2])})
RETURN a.name, a.year

MATCH (n {name: 'Andy'})
SET n.surname = 'Taylor'
RETURN n.name, n.surname

MATCH (n:Swedish {name: 'Andy'})-[r:KNOWS]->(m)
SET r.since = 1999
RETURN r, m.name AS friend

WITH 'AGE' AS propname
MATCH (n:Person)
WHERE n[toLower(propname)] < 30
RETURN n.name, n.age

MATCH (n:Person)
WHERE n.age < 30
RETURN n.name, n.age

CREATE TEXT INDEX IX:User
FOR (n:business)
ON (n.business_id)



<-- Apuntes del Neo4J

CREATE (ee:Person {name: 'Emil', from: 'Sweden', kloutScore: 99})
MATCH (ee:Person) WHERE ee.name = 'Emil' RETURN ee;

MATCH (ee:Person)-[:KNOWS]-(friends)
WHERE ee.name = 'Emil' RETURN ee, friends

CREATE CONSTRAINT FOR (n:Movie) REQUIRE (n.title) IS UNIQUE
CREATE CONSTRAINT FOR (n:Person) REQUIRE (n.name) IS UNIQUE

CREATE INDEX FOR (m:Movie) ON (m.released)

MATCH (tom:Person {name: "Tom Hanks"}) RETURN tom
MATCH (cloudAtlas:Movie {title: "Cloud Atlas"}) RETURN cloudAtlas
MATCH (people:Person) RETURN people.name LIMIT 10

MATCH (nineties:Movie) WHERE nineties.released >= 1990 AND nineties.released < 2000 RETURN nineties.title

MATCH (tom:Person {name: "Tom Hanks"})-[:ACTED_IN]->(tomHanksMovies) RETURN tom,tomHanksMovies

MATCH (cloudAtlas:Movie {title: "Cloud Atlas"})<-[:DIRECTED]-(directors) RETURN directors.name

MATCH (tom:Person {name:"Tom Hanks"})-[:ACTED_IN]->(m)<-[:ACTED_IN]-(coActors) RETURN DISTINCT coActors.name

MATCH (people:Person)-[relatedTo]-(:Movie {title: "Cloud Atlas"}) RETURN people.name, Type(relatedTo), relatedTo.roles

CALL db.schema.visualization();

MATCH (bacon:Person {name:"Kevin Bacon"})-[*1..4]-(hollywood)
RETURN DISTINCT hollywood

MATCH p=shortestPath(
(bacon:Person {name:"Kevin Bacon"})-[*]-(meg:Person {name:"Meg Ryan"})
)
RETURN p

MATCH (tom:Person {name:"Tom Hanks"})-[:ACTED_IN]->(m)<-[:ACTED_IN]-(coActors),
    (coActors)-[:ACTED_IN]->(m2)<-[:ACTED_IN]-(cocoActors)
  WHERE NOT (tom)-[:ACTED_IN]->()<-[:ACTED_IN]-(cocoActors) AND tom <> cocoActors
  RETURN cocoActors.name AS Recommended, count(*) AS Strength ORDER BY Strength DESC

MATCH (tom:Person {name:"Tom Hanks"})-[:ACTED_IN]->(m)<-[:ACTED_IN]-(coActors),
  (coActors)-[:ACTED_IN]->(m2)<-[:ACTED_IN]-(cruise:Person {name:"Tom Cruise"})
RETURN tom, m, coActors, m2, cruise

MATCH (n) DETACH DELETE n

LOAD CSV WITH HEADERS FROM "https://data.neo4j.com/northwind/products.csv" AS row
CREATE (n:Product)
SET n = row,
n.unitPrice = toFloat(row.unitPrice),
n.unitsInStock = toInteger(row.unitsInStock), n.unitsOnOrder = toInteger(row.unitsOnOrder),
n.reorderLevel = toInteger(row.reorderLevel), n.discontinued = (row.discontinued <> "0")

MATCH (cust:Customer)-[:PURCHASED]->(:Order)-[o:ORDERS]->(p:Product),
  (p)-[:PART_OF]->(c:Category {categoryName:"Produce"})
RETURN DISTINCT cust.contactName as CustomerName, SUM(o.quantity) AS TotalProductsPurchased


1. Encuentra todos los amigos de un usuario
MATCH (u:User {name: "Alice"})-[:FRIEND]->(friend:User)
RETURN friend.name AS FriendName;


2. Encuentra amigos de amigos que no sean amigos directos
MATCH (u:User {name: "Alice"})-[:FRIEND]->(friend:User)-[:FRIEND]->(fof:User)
WHERE NOT (u)-[:FRIEND]->(fof)
RETURN fof.name AS SuggestedFriend;


3. Encuentra el camino más corto entre dos usuarios
MATCH p=shortestPath((u1:User {name: "Alice"})-[:FRIEND*]-(u2:User {name: "Bob"}))
RETURN p;


4. Películas dirigidas por directores que también son actores
MATCH (d:Director)-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(d)
RETURN d.name AS DirectorActor, m.title AS MovieTitle;


5. Encuentra películas con actores que trabajaron juntos más de 3 veces
MATCH (a1:Actor)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(a2:Actor)
WHERE a1 <> a2
WITH a1, a2, COUNT(m) AS moviesTogether
WHERE moviesTogether > 3
RETURN a1.name AS Actor1, a2.name AS Actor2, moviesTogether;


6. Usuarios con la mayor cantidad de conexiones
MATCH (u:User)-[:FRIEND]->(friend:User)
WITH u, COUNT(friend) AS numFriends
ORDER BY numFriends DESC
RETURN u.name AS UserName, numFriends
LIMIT 1;


7. Encuentra recomendaciones de películas basadas en amigos
MATCH (u:User {name: "Alice"})-[:FRIEND]->(friend:User)-[:LIKED]->(movie:Movie)
WHERE NOT (u)-[:LIKED]->(movie)
RETURN movie.title AS RecommendedMovie, COUNT(friend) AS Popularity
ORDER BY Popularity DESC;


8. Detecta ciclos en una red social
MATCH p=(u:User)-[:FRIEND*]-(u)
WHERE LENGTH(p) > 2
RETURN DISTINCT p;


9. Encuentra comunidades usando algoritmos de grafos
CALL gds.graph.project(
  'socialGraph',
  'User',
  {
    FRIEND: {
      type: 'FRIEND',
      properties: {}
    }
  }
);

CALL gds.louvain.stream('socialGraph')
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).name AS UserName, communityId
ORDER BY communityId;


10. Encuentra todas las películas populares (con más de 3 "me gusta")
MATCH (m:Movie)<-[:LIKED]-(u:User)
WITH m, COUNT(u) AS numLikes
WHERE numLikes > 3
RETURN m.title AS PopularMovie, numLikes
ORDER BY numLikes DESC;

