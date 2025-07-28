from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import os
from model import TeaLeafClassifier 
from flask import jsonify
import os

base_dir = "dataset"
print("[DEBUG] Path absolute:", os.path.abspath(base_dir))
if not os.path.exists(base_dir):
    raise FileNotFoundError(f"Folder '{base_dir}' tidak ditemukan.")


app = Flask(__name__)
CORS(app)

# Load model
classifier = TeaLeafClassifier()
classifier.load_model("knn_model.pkl")

@app.route('/api/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No image uploaded'}), 400
    
    image_file = request.files['image']
    filename = secure_filename(image_file.filename)
    image_path = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    image_file.save(image_path)

    # Load & predict
    image = cv2.imread(image_path)
    result = classifier.predict(image)

    if result['class'] == "non_tea":
        return jsonify({
            "status": "non_tea",
            "message": "Gambar ini bukan daun teh."
        }), 200
    else:
        return jsonify({
            "status": "daun_teh",
            "kematangan": result['class'].lower()
        }), 200

if __name__ == '__main__':
    app.run(debug=True)
