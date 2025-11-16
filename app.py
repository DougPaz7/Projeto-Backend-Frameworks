from flask import Flask, jsonify, request
from controllers.tasks_controller import tasks_bp

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "status": "online",
        "message": "Minha API de To-Do está pronta!"
    })

app.register_blueprint(tasks_bp, url_prefix='/tasks')