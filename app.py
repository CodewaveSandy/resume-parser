from flask import Flask, jsonify, request
from dotenv import load_dotenv
from pyresparser import ResumeParser
import traceback
import os

load_dotenv()  # ✅ Load variables from .env into os.environ

app = Flask(__name__)
API_KEY = os.environ.get("API_KEY")
port = int(os.environ.get("PORT", 3002)) 

@app.before_request
def check_api_key():
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

@app.route("/parse", methods=["POST"])
def parse_resume():
    if 'file' not in request.files:
        print("❌ No file in request")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filename = file.filename
    temp_path = f"/tmp/{filename}"
    file.save(temp_path)

    print(f"📄 Received file: {filename}")
    print(f"🛠️  Saved temporarily at: {temp_path}")

    try:
        data = ResumeParser(temp_path).get_extracted_data()
        print("✅ Parsing complete:")
        print(data)
        return jsonify({
            "message": "Resume parsed successfully",
            "data": data
        })
    except Exception as e:
        print("🔥 Exception occurred during parsing:")
        traceback.print_exc()  # Full stack trace in logs
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"🧹 Temp file deleted: {temp_path}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

