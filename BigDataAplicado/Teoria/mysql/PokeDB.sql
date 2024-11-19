CREATE DATABASE PokeDB;
USE PokeDB;

CREATE TABLE Trainers (
    TrainerID INT AUTO_INCREMENT PRIMARY KEY ,
    TrainerName VARCHAR(50) NOT NULL,
    Age INT
);

CREATE TABLE Pokemons (
    PokemonID INT AUTO_INCREMENT PRIMARY KEY,
    PokemonName VARCHAR(50) NOT NULL
);

CREATE TABLE Badges (
    BadgeID INT AUTO_INCREMENT PRIMARY KEY,
    BadgeName VARCHAR(50) NOT NULL,
    TrainerID INT UNIQUE,
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID) ON DELETE CASCADE
);

CREATE TABLE Abilities (
    AbilityID INT AUTO_INCREMENT PRIMARY KEY,
    AbilityName VARCHAR(50) NOT NULL
);

CREATE TABLE PokemonAbilities (
    PokemonID INT,
    AbilityID INT,
    PRIMARY KEY (PokemonID, AbilityID),
    FOREIGN KEY (PokemonID) REFERENCES Pokemons(PokemonID) ON DELETE CASCADE,
    FOREIGN KEY (AbilityID) REFERENCES Abilities(AbilityID) ON DELETE CASCADE
);

CREATE TABLE Battles (
    BattleID INT AUTO_INCREMENT PRIMARY KEY,
    Trainer1ID INT,
    Trainer2ID INT,
    WinnerTrainerID INT,
    BattleDate DATETIME,
    FOREIGN KEY (Trainer1ID) REFERENCES Trainers(TrainerID) ON DELETE CASCADE,
    FOREIGN KEY (Trainer2ID) REFERENCES Trainers(TrainerID) ON DELETE CASCADE,
    FOREIGN KEY (WinnerTrainerID) REFERENCES Trainers(TrainerID) ON DELETE SET NULL
);

CREATE TABLE BattlePokemons (
    BattleID INT,
    PokemonID INT,
    TrainerID INT,
    PRIMARY KEY (BattleID, PokemonID, TrainerID),
    FOREIGN KEY (BattleID) REFERENCES Battles(BattleID) ON DELETE CASCADE,
    FOREIGN KEY (PokemonID) REFERENCES Pokemons(PokemonID) ON DELETE CASCADE,
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID) ON DELETE CASCADE
);

INSERT INTO Trainers (TrainerName, Age) VALUES ('Ash', 10), ('Misty', 15), ('Brock', 20), ('Gary', 25), ('May', 18), ('Andrei',24);

SELECT * FROM Trainers;

INSERT INTO Pokemons (PokemonName) VALUES ('Pikachu'), ('Bulbasaur'), ('Charmander'), ('Squirtle'), ('Jigglypuff'),('Snorlax'),('Mewtwo'),('Gengar'),('Dragonite'),('Moltres'),('Eevee'), ('Vaporeon'), ('Flareon'), ('Jolteon'), ('Espeon'),('Umbreon'),('Leafeon'),('Glaceon'),('Sylveon'),('Venusaur')

SELECT * FROM Pokemons;

INSERT INTO Badges (BadgeName, TrainerID) VALUES ('Kanto', 1), ('Johto', 2), ('Hoenn', 3), ('Sinnoh', 4), ('Unova', 5);

SELECT * FROM Badges;

INSERT INTO Abilities (AbilityName) VALUES ('Static'), ('Thunderbolt'), ('Overgrow'), ('Chlorophyll'), ('Synchronize');

SELECT * FROM Abilities;

INSERT INTO PokemonAbilities (PokemonID, AbilityID) VALUES (1, 1), (2, 2), (3, 3), (4, 4), (5, 5);

SELECT * FROM PokemonAbilities;

INSERT INTO Battles (Trainer1ID, Trainer2ID, WinnerTrainerID, BattleDate) VALUES (1, 2, 1, '2023-01-01'), (3, 4, 3, '2023-02-01'), (5, 1, 5, '2023-03-01'), (2, 3, 2, '2023-04-01'), (4, 5, 4, '2023-05-01');

SELECT * FROM Battles;

INSERT INTO BattlePokemons (BattleID, PokemonID, TrainerID) VALUES (1, 1, 1), (1, 2, 1), (2, 3, 3), (2, 4, 3), (3, 5, 5), (3, 6, 5), (4, 7, 2), (4, 8, 2), (5, 9, 4);

SELECT * FROM BattlePokemons;

/* Solo poner left o right joins cuando son nullables */
-- PRUEBAS DE CONSULTAS --
-- Select all trainers.
SELECT * FROM Trainers;
-- Find all Pokémon names.
SELECT PokemonName FROM Pokemons;
-- Count the number of Pokémon each trainer has.
SELECT t.TrainerName,Count(distinct bp.PokemonID) as numPokemons FROM Trainers AS t 
LEFT JOIN BattlePokemons AS bp ON t.TrainerID = bp.TrainerID GROUP BY  t.TrainerID,t.TrainerName;
-- List all badges with their corresponding trainer names.
SELECT b.BadgeName, t.TrainerName FROM Badges AS b LEFT JOIN Trainers AS t ON b.TrainerID = t.TrainerID;
-- Get all abilities.
SELECT AbilityName FROM Abilities;
-- Find all battles and their winners.
SELECT b.BattleID, b.BattleDate, t.TrainerName FROM Battles b LEFT JOIN Trainers t on b.WinnerTrainerID=t.TrainerID;
-- Get all Pokémon associated with a specific battle (e.g., BattleID = 1).
SELECT Pokemons.PokemonName FROM BattlePokemons JOIN Pokemons ON BattlePokemons.PokemonID = Pokemons.PokemonID WHERE BattleID = 1;
-- Retrieve all Pokémon of a specific trainer (e.g., TrainerID = 1).
SELECT PokemonName FROM Pokemons WHERE TrainerID = 1;
-- List all trainers who have at least one badge.
SELECT TrainerName FROM Trainers WHERE TrainerID IN (SELECT TrainerID FROM Badges);
-- Count the number of battles each trainer has participated in.
SELECT count(distinct BattlePokemons.BattleID) as NumeroBatallas,Trainers.TrainerName FROM BattlePokemons INNER JOIN Trainers ON BattlePokemons.TrainerID = Trainers.TrainerID GROUP BY Trainers.TrainerID;
--List all badges and trainers who have them, including trainers without badges (LEFT JOIN).
SELECT * FROM Trainers LEFT JOIN Badges ON Trainers.TrainerID=Badges.TrainerID;
--Find all trainers and their Pokémon, including trainers without Pokémon (LEFT JOIN).
SELECT * FROM Trainers LEFT JOIN BattlePokemons ON Trainers.TrainerID=BattlePokemons.TrainerID;
--Get a list of trainers and their badges, including badges without trainers (RIGHT JOIN).
SELECT Trainers.TrainerName, Badges.BadgeName FROM Trainers RIGHT JOIN Badges ON Trainers.TrainerID=Badges.TrainerID;
--Combine trainers who have at least one Pokémon and those who have badges (UNION).

--Get all trainers who have Pokémon or badges (INTERSECT).

--Find all trainers with their Pokémon and abilities using multiple joins.

--Find the trainer with the most Pokémon.
SELECT t.TrainerName,Count(distinct bp.PokemonID) as numPokemons FROM Trainers AS t
LEFT JOIN BattlePokemons AS bp ON t.TrainerID = bp.TrainerID GROUP BY  t.TrainerID,t.TrainerName ORDER BY numPokemons;
--List all battles that occurred on a specific date (e.g., '2024-01-01').
SELECT * FROM Battles WHERE BattleDate='2024-01-01';
--Retrieve all Pokémon names along with their abilities.
SELECT * FROM Pokemons JOIN PokemonAbilities ON Pokemons.PokemonID=PokemonAbilities.PokemonID JOIN Abilities ON PokemonAbilities.AbilityID=Abilities.AbilityID;
--Get all trainers who won a battle.
SELECT * FROM Trainers WHERE TrainerID IN (SELECT WinnerTrainerID FROM Battles);
--Scalar Subquery: Find the number of badges for a specific trainer (e.g., TrainerID = 1).

--Multiple-Row Subquery: Retrieve all trainers who have more Pokémon than the average number of Pokémon per trainer.

--Correlated Subquery: List all trainers who have more Pokémon than the trainer with the least number of Pokémon.

--Correlated Subquery: Find all battles where Trainer1 has more Pokémon than Trainer2.

--Multiple-Row Subquery: List all Pokémon that have abilities not held by any Pokémon in a specific battle (e.g., BattleID = 1).
