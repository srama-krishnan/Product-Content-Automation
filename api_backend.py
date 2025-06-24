from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import os
import datetime
from main import generate_product_json  # We'll refactor main.py to expose this

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        print("✅ Request received:", data)

        # Call your main logic
        result = generate_product_json(data)

        return jsonify(result)

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
