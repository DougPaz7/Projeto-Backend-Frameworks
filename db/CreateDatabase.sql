CREATE DATABASE todo_db;

USE todo_db;

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SET character_set_client = utf8;
SET character_set_connection = utf8;
SET character_set_results = utf8;
SET collation_connection = utf8_general_ci;

INSERT INTO tasks (title, completed) VALUES ('Minha tarefa já concluída', 1);
INSERT INTO tasks (title, completed) VALUES ('Minha tarefa já incompleta', 0);
INSERT INTO tasks (title, completed) VALUES ('Minha outra tarefa', 0);