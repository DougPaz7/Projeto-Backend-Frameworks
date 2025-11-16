from flask import Blueprint, jsonify, request
from mysql.connector import Error
from db import get_connection 

tasks_bp = Blueprint('tasks_api', __name__)

@tasks_bp.route("/", methods=['GET'])
def get_tasks():
    tasks = []
    conn = None
    cursor = None

    
    try:
        title_filter = request.args.get('title')
        completed_filter = request.args.get('completed')

        conn = get_connection()
        
        if conn is None:
            return jsonify({"error": "Failed to connect to the database"}), 500
        
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM tasks"
        where_clauses = []
        values = []

        if title_filter:
            where_clauses.append("title LIKE %s")
            values.append(f"%{title_filter}%")

        if completed_filter is not None:
            if completed_filter.lower() in ['true', '1']:
                where_clauses.append("completed = %s")
                values.append(1)
            elif completed_filter.lower() in ['false', '0']:
                where_clauses.append("completed = %s")
                values.append(0)
        
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)
            
        sql += " ORDER BY created_at DESC"

        cursor.execute(sql, tuple(values))
        tasks = cursor.fetchall()
        
        for task in tasks:
            if 'created_at' in task and task['created_at']:
                task['created_at'] = task['created_at'].isoformat()
    
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return jsonify({"error": "Error fetching tasks"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return jsonify(tasks)

@tasks_bp.route("/<int:id>", methods=['GET'])
def get_task_by_id(id):
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        if conn is None:
            return jsonify({"error": "Failed to connect to the database"}), 500
        
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM tasks WHERE id = %s"
        values = (id,)
        
        cursor.execute(sql, values)

        task = cursor.fetchone()

        if task is None:
            return jsonify({"error": "Task not found"}), 404
        
        if task['created_at']:
            task['created_at'] = task['created_at'].isoformat()

        return jsonify(task), 200

    except Error as e:
        print(f"Error fetching task: {e}")
        return jsonify({"error": "Error fetching task"}), 500
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@tasks_bp.route("/", methods=['POST'])
def create_task():
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({"error": "the 'title' is must be required"}), 400

    title = data['title']
    
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        if conn is None:
            return jsonify({"error": "Failed to connect to the database"}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        sql = "INSERT INTO tasks (title) VALUES (%s)"
        values = (title,)
        
        cursor.execute(sql, values)
        
        conn.commit()
        
        new_task_id = cursor.lastrowid
        
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (new_task_id,))
        new_task = cursor.fetchone()
        
        if new_task and 'created_at' in new_task and new_task['created_at']:
             new_task['created_at'] = new_task['created_at'].isoformat()
        
        return jsonify(new_task), 201 

    except Exception as e:
        print(f"Error creating task: {e}")

        if conn:
            conn.rollback()
        return jsonify({"error": "Error creating task"}), 500
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@tasks_bp.route("/<int:id>", methods=['PUT'])
def update_task(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "data is must me required"}), 400

    if 'title' not in data and 'completed' not in data:
        return jsonify({"error": "No valid field ('title' or 'completed') provided"}), 400

    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        if conn is None:
            return jsonify({"error": "Failed to connect to the database"}), 500
        
        cursor = conn.cursor(dictionary=True)
        
        fields_to_update = []
        values = []

        if 'title' in data:
            fields_to_update.append("title = %s")
            values.append(data['title'])
            
        if 'completed' in data:
            fields_to_update.append("completed = %s")
            values.append(data['completed'])

        sql_set_clause = ", ".join(fields_to_update)

        values.append(id) 
        
        sql = f"UPDATE tasks SET {sql_set_clause} WHERE id = %s"
        
        cursor.execute(sql, tuple(values))

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found or data the same"}), 404

        cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))
        updated_task = cursor.fetchone()
        
        if updated_task['created_at']:
            updated_task['created_at'] = updated_task['created_at'].isoformat()

        return jsonify(updated_task), 200

    except Error as e:
        print(f"Error updating task: {e}")
        if conn:
            conn.rollback()
        return jsonify({"error": "Error updating task"}), 500
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@tasks_bp.route("/<int:id>", methods=['DELETE'])
def delete_task(id):
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        if conn is None:
            return jsonify({"error": "Failed to connect to the database"}), 500
        
        cursor = conn.cursor()

        sql = "DELETE FROM tasks WHERE id = %s"
        values = (id,)
        
        cursor.execute(sql, values)

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

        return jsonify({"message": "Task deleted successfully"}), 200

    except Error as e:
        print(f"Error deleting task: {e}")
        if conn:
            conn.rollback()
        return jsonify({"error": "Error deleting task"}), 500
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()