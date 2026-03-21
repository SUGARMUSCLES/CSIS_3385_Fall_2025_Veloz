@'
import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Load seed data (seed.json expected in repo root)
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) if os.path.basename(os.getcwd()).lower() == "project2" else os.path.dirname(__file__)
seed_path = os.path.join(BASE_DIR, "seed.json")

try:
    with open(seed_path, "r", encoding="utf8") as f:
        raw_users = json.load(f)
except FileNotFoundError:
    raw_users = []

# Normalize users to expected internal keys
users = [
    {
        "id": u.get("id"),
        "username": u.get("username"),
        "password": u.get("password"),
        "email": u.get("email"),
        "age": u.get("age")
    } for u in raw_users
]

# GET all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

# POST create user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(force=True)
    new_user = {
        "id": (max([u["id"] for u in users]) + 1) if users else 1,
        "username": data.get("username"),
        "email": data.get("email"),
        "age": data.get("age"),
        "password": data.get("password")
    }
    users.append(new_user)
    return jsonify(new_user), 201

# PUT update user by id
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json(force=True)
    for user in users:
        if user["id"] == user_id:
            user["username"] = data.get("username", user["username"])
            user["email"] = data.get("email", user["email"])
            user["age"] = data.get("age", user["age"])
            user["password"] = data.get("password", user["password"])
            return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

# DELETE user by id
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": f"User {user_id} deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
'@ | Out-File -FilePath .\Project2\app.py -Encoding utf8

# 3) Start the Flask app using the venv Python (run from repo root)
.\venv\Scripts\python.exe .\Project2\app.py
