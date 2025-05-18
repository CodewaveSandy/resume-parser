from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import re
import textract
import traceback

load_dotenv()

app = Flask(__name__)
API_KEY = os.environ.get("API_KEY")
port = int(os.environ.get("PORT", 3002))


@app.before_request
def check_api_key():
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401


def extract_text(file_path):
    return textract.process(file_path).decode("utf-8", errors="ignore")


def extract_personal_info(text):
    def extract_name(text):
        lines = text.splitlines()
        lines = [line.strip() for line in lines if line.strip()]
        for line in lines[:5]:
            if "@" not in line and not re.search(r"\d", line) and len(line.split()) <= 4:
                return line
        return None

    def extract_email(text):
        match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', text)
        return match.group(0) if match else None

    def extract_phone(text):
        match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        return match.group(0) if match else None

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text)
    }


@app.route("/parse", methods=["POST"])
def parse_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filename = file.filename
    temp_path = f"/tmp/{filename}"
    file.save(temp_path)

    try:
        text = extract_text(temp_path)
        data = extract_personal_info(text)

        return jsonify({
            "message": "Personal info extracted successfully",
            "data": data
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
