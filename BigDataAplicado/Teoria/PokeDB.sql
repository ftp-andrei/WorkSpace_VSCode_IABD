CREATE TABLE Trainers (
    TrainerID INT AUTO_INCREMENT PRIMARY KEY,
    TrainerName VARCHAR(50) NOT NULL,
    Age INT
);

CREATE TABLE Pokemons (
    PokemonID INT AUTO_INCREMENT PRIMARY KEY,
    PokemonName VARCHAR(50) NOT NULL,
    TrainerID INT,
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID) ON DELETE SET NULL
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
    PRIMARY KEY (BattleID, PokemonID),
    FOREIGN KEY (BattleID) REFERENCES Battles(BattleID) ON DELETE CASCADE,
    FOREIGN KEY (PokemonID) REFERENCES Pokemons(PokemonID) ON DELETE CASCADE,
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerID) ON DELETE CASCADE
);



INSERT INTO Trainers (TrainerName, Age) VALUES ('Ash', 10), ('Misty', 15), ('Brock', 20), ('Gary', 25), ('May', 18), ('Andrei',24);

SELECT * FROM Trainers;

INSERT INTO Pokemons (PokemonName, TrainerID) VALUES ('Pikachu', 1), ('Charizard', 2), ('Bulbasaur', 3), ('Squirtle', 4), ('Jigglypuff', 5), ('Eevee', 1), ('Snorlax', 2), ('Mewtwo', 3), ('Gyarados', 4), ('Lugia', 5), ('Dialga', 1), ('Palkia', 2), ('Groudon', 3), ('Kyogre', 4), ('Rayquaza', 5);

SELECT * FROM Pokemons;

INSERT INTO Badges (BadgeName, TrainerID) VALUES ('Kanto', 1), ('Johto', 2), ('Hoenn', 3), ('Sinnoh', 4), ('Unova', 5);

SELECT * FROM Badges;

INSERT INTO Abilities (AbilityName) VALUES ('Static'), ('Thunderbolt'), ('Overgrow'), ('Chlorophyll'), ('Synchronize');

SELECT * FROM Abilities;

INSERT INTO PokemonAbilities (PokemonID, AbilityID) VALUES (1, 1), (2, 2), (3, 3), (4, 4), (5, 5);

SELECT * FROM PokemonAbilities;

INSERT INTO Battles (Trainer1ID, Trainer2ID, WinnerTrainerID, BattleDate) VALUES (1, 2, 1, '2023-01-01'), (3, 4, 3, '2023-02-01'), (5, 1, 5, '2023-03-01'), (2, 3, 2, '2023-04-01'), (4, 5, 4, '2023-05-01');

SELECT * FROM Battles;

INSERT INTO BattlePokemons (BattleID, PokemonID, TrainerID) VALUES (1, 1, 1), (1, 2, 2), (2, 3, 3), (2, 4, 4), (3, 5, 5), (3, 1, 1), (4, 2, 2), (4, 3, 3), (5, 4, 4);

SELECT * FROM BattlePokemons;


-- PRUEBAS DE CONSULTAS --
-- Select all trainers.
SELECT * FROM Trainers;
-- Find all Pokémon names.
SELECT PokemonName FROM Pokemons;
-- Count the number of Pokémon each trainer has.
SELECT count(Pokemons.PokemonName) AS PokemonCount, Trainers.TrainerName FROM Trainers LEFT JOIN Pokemons ON Pokemons.TrainerID = Trainers.TrainerID GROUP BY Trainers.TrainerName;
-- List all badges with their corresponding trainer names.
SELECT BadgeName, TrainerName FROM Badges LEFT JOIN Trainers ON Badges.TrainerID = Trainers.TrainerID;
-- Get all abilities.
SELECT AbilityName FROM Abilities;
-- Find all battles and their winners.
SELECT BattleID, WinnerTrainerID FROM Battles;
-- Get all Pokémon associated with a specific battle (e.g., BattleID = 1).
SELECT PokemonID FROM BattlePokemons WHERE BattleID = 1;
-- Retrieve all Pokémon of a specific trainer (e.g., TrainerID = 1).
SELECT PokemonName FROM Pokemons WHERE TrainerID = 1;
-- List all trainers who have at least one badge.
SELECT TrainerName FROM Trainers WHERE TrainerID IN (SELECT TrainerID FROM Badges);
-- Count the number of battles each trainer has participated in.

