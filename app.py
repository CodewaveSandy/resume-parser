from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

load_dotenv()  # ✅ Load variables from .env into os.environ

app = Flask(__name__)
API_KEY = os.environ.get("API_KEY")

@app.before_request
def check_api_key():
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

@app.route("/parse", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from Python"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
