from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import re
import textract
import traceback
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
API_KEY = os.environ.get("API_KEY")
port = int(os.environ.get("PORT", 3002))


@app.before_request
def check_api_key():
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        logger.warning("Unauthorized access attempt.")
        return jsonify({"error": "Unauthorized"}), 401


def extract_text(file_path):
    return textract.process(file_path).decode("utf-8", errors="ignore")


def extract_personal_info(text):
    def extract_name(text):
        lines = text.splitlines()
        lines = [line.strip() for line in lines if line.strip()]

        first_name = middle_name = last_name = surname = full_name = None

        for line in lines[:20]:
            lower = line.lower()

            if "first name" in lower:
                match = re.search(r'first name\s*[:\-–]\s*(.*)', line, re.I)
                if match:
                    first_name = match.group(1).strip()

            elif "middle name" in lower:
                match = re.search(r'middle name\s*[:\-–]\s*(.*)', line, re.I)
                if match:
                    middle_name = match.group(1).strip()

            elif "last name" in lower:
                match = re.search(r'last name\s*[:\-–]\s*(.*)', line, re.I)
                if match:
                    last_name = match.group(1).strip()

            elif "surname" in lower:
                match = re.search(r'surname\s*[:\-–]\s*(.*)', line, re.I)
                if match:
                    surname = match.group(1).strip()

            elif re.match(r'(?i)^name\s*[:\-–]\s*', line):
                full_name = re.sub(r'(?i)^name\s*[:\-–]\s*', '', line).strip()

            elif re.match(r'(?i)^full name\s*[:\-–]\s*', line):
                full_name = re.sub(r'(?i)^full name\s*[:\-–]\s*', '', line).strip()

        if first_name:
            parts = [first_name]
            if middle_name:
                parts.append(middle_name)
            if last_name:
                parts.append(last_name)
            elif surname:
                parts.append(surname)
            return " ".join(parts)

        return full_name or None

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
        logger.info(f"Parsing file: {filename}")
        text = extract_text(temp_path)
        logger.info("Text extraction successful.")
        data = extract_personal_info(text)
        logger.info(f"Extracted Data: {data}")


        return jsonify({
            "message": "Personal info extracted successfully",
            "data": data
        })
    except Exception as e:
        traceback.print_exc()
        logger.error("Exception during resume parsing", exc_info=True)
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            logger.info(f"Temporary file deleted: {temp_path}")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
