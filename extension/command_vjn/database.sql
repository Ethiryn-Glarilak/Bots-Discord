DROP TABLE IF EXISTS product_ingredient_VJN, command_VJN, product_VJN, ingredient_VJN;

CREATE TABLE product_VJN
    (
        id              SERIAL PRIMARY KEY,
        name            VARCHAR(255) NOT NULL,
        price           MONEY NOT NULL
    );

CREATE TABLE command_VJN
    (
        id              SERIAL PRIMARY KEY,
        id_user         BIGINT NOT NULL,
        id_product      INT REFERENCES product_VJN(id),
        date            DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        price           MONEY,
        status          INT NOT NULL
    );

CREATE TABLE ingredient_VJN
    (
        id              SERIAL PRIMARY KEY,
        name            VARCHAR(255) NOT NULL,
        price           MONEY,
        quantities      INT
    );

CREATE TABLE product_ingredient_VJN
    (
        id_product      INT REFERENCES product_VJN(id),
        id_ingredient   INT REFERENCES ingredient_VJN(id)
    );

INSERT INTO product_VJN (name, price) VALUES
    ('Confiture Fraise Nutella', 2.2),
    ('Miel Banane', 2.2),
    ('Nutella Banane', 2.2),
    ('Confiture Fraise Banane', 2.2),
    ('Sucre Beurre', 1.3),
    ('Miel', 1.7),
    ('Nutella', 1.7),
    ('Confiture Fraise', 1.7),
    ('Banane', 1.2),
    ('Sucre', 1),
    ('Pate Uniquement', 0.7),
    ('Emmental Raclette', 3.7),
    ('Emmental Raclette Oeuf', 4.2),
    ('Oeuf', 1.2),
    ('Raclette', 2.2),
    ('Emmental', 2.2),
    ('Raclette Oeuf', 2.7),
    ('Emmental Oeuf', 2.7),
    ('Jambon Emmental Raclette', 5.2),
    ('Jambon Emmental Raclette Oeuf', 5.7),
    ('Jambon Oeuf', 2.7),
    ('Jambon Raclette', 3.7),
    ('Jambon Emmental', 3.7),
    ('Jambon Raclette Oeuf', 4.2),
    ('Jambon Emmental Oeuf', 4.2),
    ('Poulet Emmental Raclette', 5.2),
    ('Poulet Emmental Raclette Oeuf', 5.7),
    ('Poulet Oeuf', 2.7),
    ('Poulet Raclette', 3.7),
    ('Poulet Emmental', 3.7),
    ('Poulet Raclette Oeuf', 4.2),
    ('Poulet Emmental Oeuf', 4.2),
    ('Jambon Poulet Emmental Raclette', 6.7),
    ('Jambon Poulet Emmental Raclette Oeuf', 7.2),
    ('Jambon Poulet Oeuf', 4.2),
    ('Jambon Poulet Raclette', 5.2),
    ('Jambon Poulet Emmental', 5.2),
    ('Jambon Poulet Raclette Oeuf', 5.7),
    ('Jambon Poulet Emmental Oeuf', 5.7);

INSERT INTO ingredient_VJN (name, price) VALUES
    ('Pate Bière', 0),
    ('Pate Nature', 0),
    ('Confiture Fraise', 0),
    ('Nutella', 0),
    ('Miel', 0),
    ('Banane', 0),
    ('Sucre', 0),
    ('Beurre', 0),
    ('Emmental', 0),
    ('Raclette', 0),
    ('Oeuf', 0),
    ('Jambon', 0),
    ('Poulet', 0);

INSERT INTO product_ingredient_VJN (id_product, id_ingredient) VALUES
    (1, 3),(1, 4),
    (2, 5),(2, 6),
    (3, 4),(3, 6),
    (4, 3),(4, 6),
    (5, 7),(5, 8),
    (6, 5),
    (7, 4),
    (8, 3),
    (9, 6),
    (10, 7),
    (11, 2),
    (12, 9),(12, 10),
    (13, 9),(13, 10),(13, 11),
    (14, 11),
    (15, 10),
    (16, 9),
    (17, 10),(17, 11),
    (18, 9),(18, 11),
    (19, 12),(19, 9),(19, 10),
    (20, 12),(20, 9),(20, 10),(20, 11),
    (21, 12),(21, 11),
    (22, 12),(22, 10),
    (23, 12),(23, 9),
    (24, 12),(24, 10),(24, 11),
    (25, 12),(25, 9),(25, 11),
    (26, 13),(26, 9),(26, 10),
    (27, 13),(27, 9),(27, 10),(27, 11),
    (28, 13),(28, 11),
    (29, 13),(29, 10),
    (30, 13),(30, 9),
    (31, 13),(31, 10),(31, 11),
    (32, 13),(32, 9),(32, 11),
    (33, 12),(33, 13),(33, 9),(33, 10),
    (34, 12),(34, 13),(34, 9),(34, 10),(34, 11),
    (35, 12),(35, 13),(35, 11),
    (36, 12),(36, 13),(36, 10),
    (37, 12),(37, 13),(37, 9),
    (38, 12),(38, 13),(38, 10),(38, 11),
    (39, 12),(39, 13),(39, 9),(39, 11);
