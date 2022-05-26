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
        quantities      INT
    );

CREATE TABLE product_ingredient_VJN
    (
        id_product      INT REFERENCES product_VJN(id),
        id_ingredient   INT REFERENCES ingredient_VJN(id)
    );

INSERT INTO product_VJN (name, price) VALUES
    ('Confiture Fraise Nutella', 0),
    ('Miel Banane', 0),
    ('Nutella Banane', 0),
    ('Confiture Fraise Banane', 0),
    ('Sucre Beurre', 0),
    ('Miel', 0),
    ('Nutella', 0),
    ('Confiture Fraise', 0),
    ('Banane', 0),
    ('Sucre', 0),
    ('Pate Uniquement', 0),
    ('Emmental Raclette', 0),
    ('Emmental Raclette Oeuf', 0),
    ('Oeuf', 0),
    ('Raclette', 0),
    ('Emmental', 0),
    ('Raclette Oeuf', 0),
    ('Emmental Oeuf', 0),
    ('Jambon Emmental Raclette', 0),
    ('Jambon Emmental Raclette Oeuf', 0),
    ('Jambon Oeuf', 0),
    ('Jambon Raclette', 0),
    ('Jambon Emmental', 0),
    ('Jambon Raclette Oeuf', 0),
    ('Jambon Emmental Oeuf', 0),
    ('Poulet Emmental Raclette', 0),
    ('Poulet Emmental Raclette Oeuf', 0),
    ('Poulet Oeuf', 0),
    ('Poulet Raclette', 0),
    ('Poulet Emmental', 0),
    ('Poulet Raclette Oeuf', 0),
    ('Poulet Emmental Oeuf', 0),
    ('Jambon Poulet Emmental Raclette', 0),
    ('Jambon Poulet Emmental Raclette Oeuf', 0),
    ('Jambon Poulet Oeuf', 0),
    ('Jambon Poulet Raclette', 0),
    ('Jambon Poulet Emmental', 0),
    ('Jambon Poulet Raclette Oeuf', 0),
    ('Jambon Poulet Emmental Oeuf', 0);

INSERT INTO ingredient_VJN (name) VALUES
    ('Pate Bière'),
    ('Pate Nature'),
    ('Confiture Fraise'),
    ('Nutella'),
    ('Miel'),
    ('Banane'),
    ('Sucre'),
    ('Beurre'),
    ('Emmental'),
    ('Raclette'),
    ('Oeuf'),
    ('Jambon'),
    ('Poulet');

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
