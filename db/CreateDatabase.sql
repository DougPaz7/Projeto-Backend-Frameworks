CREATE DATABASE projeto;

USE projeto;

CREATE TABLE carros (
    id integer not null auto_increment,
    marca varchar(100),
    modelo varchar(100),
    ano integer,
    PRIMARY KEY (id)
);

SET character_set_client = utf8;
SET character_set_connection = utf8;
SET character_set_results = utf8;
SET collation_connection = utf8_general_ci;

INSERT INTO carros (marca, modelo, ano) VALUES ('Fiat', 'Marea', 1999);
INSERT INTO carros (marca, modelo, ano) VALUES ('Fiat', 'Uno', 1992);
INSERT INTO carros (marca, modelo, ano) VALUES ('Ford', 'Escort', 1985);
INSERT INTO carros (marca, modelo, ano) VALUES ('Chevrolet', 'Chevette', 1978);
INSERT INTO carros (marca, modelo, ano) VALUES ('Volkswagen', 'Fusca', 1962);