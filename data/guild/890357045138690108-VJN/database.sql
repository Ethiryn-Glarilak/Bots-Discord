DROP TABLE IF EXISTS product_ingredient_VJN, command_VJN, product_VJN, ingredient_VJN;

CREATE TABLE product_VJN
    (
        id              SERIAL PRIMARY KEY,
        name            VARCHAR(255) NOT NULL,
        price           MONEY NOT NULL,
        type            BOOLEAN NOT NULL DEFAULT FALSE
    );

CREATE TABLE command_VJN
    (
        id              SERIAL PRIMARY KEY,
        id_user         BIGINT NOT NULL,
        id_product      INT REFERENCES product_VJN(id),
        date            DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        price           MONEY,
        status          INT NOT NULL,
        quantity        INT NOT NULL DEFAULT 0,
        ready           INT NOT NULL DEFAULT 0
    );

CREATE TABLE ingredient_VJN
    (
        id              SERIAL PRIMARY KEY,
        name            VARCHAR(255) NOT NULL,
        price           MONEY,
        quantities      INT,
        type            BOOLEAN NOT NULL
    );

CREATE TABLE product_ingredient_VJN
    (
        id_product      INT REFERENCES product_VJN(id),
        id_ingredient   INT REFERENCES ingredient_VJN(id)
    );

INSERT INTO product_VJN (name, price, type) VALUES
    ('Confiture Fraise Nutella', 2.2, True),
    ('Miel Banane', 2.2, True),
    ('Nutella Banane', 2.2, True),
    ('Confiture Fraise Banane', 2.2, True),
    ('Sucre Beurre', 1.3, True),
    ('Miel', 1.7, True),
    ('Nutella', 1.7, True),
    ('Confiture Fraise', 1.7, True),
    ('Banane', 1.2, True),
    ('Sucre', 1, True),
    ('Pate Uniquement', 0.7, True),
    ('Emmental Raclette', 3.7, True),
    ('Emmental Raclette Oeuf', 4.2, True),
    ('Oeuf', 1.2, True),
    ('Raclette', 2.2, True),
    ('Emmental', 2.2, True),
    ('Raclette Oeuf', 2.7, True),
    ('Emmental Oeuf', 2.7, True),
    ('Jambon Emmental Raclette', 5.2, True),
    ('Jambon Emmental Raclette Oeuf', 5.7, True),
    ('Jambon Oeuf', 2.7, True),
    ('Jambon Raclette', 3.7, True),
    ('Jambon Emmental', 3.7, True),
    ('Jambon Raclette Oeuf', 4.2, True),
    ('Jambon Emmental Oeuf', 4.2, True),
    ('Poulet Emmental Raclette', 5.2, True),
    ('Poulet Emmental Raclette Oeuf', 5.7, True),
    ('Poulet Oeuf', 2.7, True),
    ('Poulet Raclette', 3.7, True),
    ('Poulet Emmental', 3.7, True),
    ('Poulet Raclette Oeuf', 4.2, True),
    ('Poulet Emmental Oeuf', 4.2, True),
    ('Jambon Poulet Emmental Raclette', 6.7, True),
    ('Jambon Poulet Emmental Raclette Oeuf', 7.2, True),
    ('Jambon Poulet Oeuf', 4.2, True),
    ('Jambon Poulet Raclette', 5.2, True),
    ('Jambon Poulet Emmental', 5.2, True),
    ('Jambon Poulet Raclette Oeuf', 5.7, True),
    ('Jambon Poulet Emmental Oeuf', 5.7, True),
    ('Chèvre Miel', 3.2, True),
    ('Spéculoos Banane', 2.2, True);

INSERT INTO ingredient_VJN (name, price, type) VALUES
    ('Pate Bière', 0.7, True),
    ('Pate Nature', 0.7, True),
    ('Confiture Fraise', 1, False),
    ('Nutella', 1, False),
    ('Miel', 1, False),
    ('Banane', 0.5, False),
    ('Sucre', 0.5, False),
    ('Beurre', 0.5, False),
    ('Emmental', 0, False),
    ('Raclette', 0, False),
    ('Oeuf', 0, False),
    ('Jambon', 0, False),
    ('Poulet', 0, False),
    ('Confiture Abricot', 1, False),
    ('Chèvre', 1.5, False),
    ('Spéculoos', 1, False);

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
    (39, 12),(39, 13),(39, 9),(39, 11),
    (40, 1),(40, 5),(40, 15),
    (41, 1),(41, 16),(41, 6);
