# API de Lista de Tarefas (To-Do List)

> Este projeto é uma API RESTful para um sistema de "To-Do List", desenvolvida como parte da avaliação da disciplina de Backend Frameworks da UNINASSAU - OLINDA.

A API permite gerenciar tarefas, cobrindo todas as operações básicas de CRUD (Criar, Ler, Atualizar, Deletar), além de incluir funcionalidades de filtragem.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **Flask:** Micro-framework web para a construção da API.
* **MySQL:** Banco de dados relacional para persistência dos dados.
* **mysql-connector-python:** Driver oficial para conexão com o MySQL.
* **Blueprints (Flask):** Para organização modular das rotas (Controllers).

---

## 📋 Requisitos Funcionais (Features)

A API atende aos seguintes requisitos funcionais:

* **[✅] RF-01:** Criar uma nova tarefa.
* **[✅] RF-02:** Listar todas as tarefas (com filtros por título e status).
* **[✅] RF-03:** Buscar uma tarefa específica por seu `id`.
* **[✅] RF-04:** Atualizar uma tarefa existente (título e/ou status).
* **[✅] RF-05:** Deletar uma tarefa específica por seu `id`.

---

## 🔌 Interface da API (Endpoints)

Abaixo estão todos os *endpoints* disponíveis na aplicação.

### 1. Listar Tarefas (com filtros)

Lista todas as tarefas. Aceita *query params* opcionais para filtragem por título (busca parcial) e status.

* **Método:** `GET`
* **URL:** `/tasks`
* **Query Params (Opcionais):**
    * `title` (string): Filtra tarefas cujo título contenha o valor.
    * `completed` (boolean): Filtra por status (`true`/`1` ou `false`/`0`).
* **Exemplos:**
    * `GET /tasks` (Lista todos)
    * `GET /tasks?title=Estudar`
    * `GET /tasks?completed=false`
    * `GET /tasks?title=Flask&completed=true`
* **Resposta (200 OK):**
    ```json
    [
      {
        "id": 1,
        "title": "Estudar Flask",
        "completed": true,
        "created_at": "2025-11-16T18:30:00"
      },
      {
        "id": 2,
        "title": "Fazer o README",
        "completed": false,
        "created_at": "2025-11-16T18:31:00"
      }
    ]
    ```

### 2. Criar Nova Tarefa

Cria uma nova tarefa. O título é obrigatório.

* **Método:** `POST`
* **URL:** `/tasks`
* **Body (JSON):**
    ```json
    {
      "title": "Minha Nova Tarefa"
    }
    ```
* **Resposta (201CREATED):**
    ```json
    {
      "id": 3,
      "title": "Minha Nova Tarefa",
      "completed": false,
      "created_at": "2025-11-16T18:32:00"
    }
    ```

### 3. Buscar Tarefa por ID

Retorna os detalhes de uma tarefa específica.

* **Método:** `GET`
* **URL:** `/tasks/1`
* **Resposta (200 OK):**
    ```json
    {
      "id": 1,
      "title": "Estudar Flask",
      "completed": true,
      "created_at": "2025-11-16T18:30:00"
    }
    ```
* **Resposta (404 Not Found):**
    ```json
    {
      "error": "Tarefa não encontrada"
    }
    ```

### 4. Atualizar Tarefa

Atualiza o `title` ou o status `completed` de uma tarefa.

* **Método:** `PUT`
* **URL:** `/tasks/1`
* **Body (JSON):** (Envie apenas os campos que deseja alterar)
    ```json
    {
      "title": "Título Atualizado",
      "completed": true
    }
    ```
* **Resposta (200 OK):**
    ```json
    {
      "id": 1,
      "title": "Título Atualizado",
      "completed": true,
      "created_at": "2025-11-16T18:30:00"
    }
    ```

### 5. Deletar Tarefa

Remove uma tarefa do banco de dados.

* **Método:** `DELETE`
* **URL:** `/tasks/1`
* **Resposta (200 OK):**
    ```json
    {
      "message": "Tarefa deletada com sucesso"
    }
    ```

---

## ▶️ Como Executar o Projeto Localmente

Siga os passos abaixo para configurar e executar a aplicação na sua máquina.

### Pré-requisitos

* Python 3.10+
* `pip` (Gerenciador de pacotes do Python)
* Um servidor MySQL (local ou remoto)

### 1. Clonar o Repositório

```bash
git clone [https://github.com/DougPaz7/Projeto-Backend-Frameworks.git](https://github.com/DougPaz7/Projeto-Backend-Frameworks.git)
cd Projeto-Backend-Frameworks
```

### 2. Criar e Ativar o Ambiente Virtual

```bash
# Criar o ambiente
python3 -m venv .venv

# Ativar (Linux/macOS)
source .venv/bin/activate
```

### 3. Instalar as Dependências

As dependências estão listadas no `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Configurar o Banco de Dados

1.  Acesse seu servidor MySQL e crie o banco de dados:
    ```sql
    CREATE DATABASE todo_db;
    ```

2.  Execute o script abaixo para criar a tabela `tasks`:
    ```sql
    USE todo_db;
    CREATE TABLE tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```

### 5. Configurar Variáveis de Ambiente

Para manter suas senhas seguras, a aplicação usa um arquivo `.env`.

1.  Renomeie o arquivo `.env.example` para `.env`:
    ```bash
    cp .env.example .env
    ```
2.  Abra o arquivo `.env` e preencha com as suas credenciais do MySQL:
    ```ini
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=sua_senha_secreta
    DB_DATABASE=todo_db
    ```

### 6. Executar a Aplicação

Com o ambiente virtual ativado, use o Flask para iniciar o servidor:

```bash
flask --app app run --debug
```

O servidor estará rodando em `http://127.0.0.1:5000`.
