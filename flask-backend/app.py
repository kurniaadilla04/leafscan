from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import os
from model import TeaLeafClassifier  # Class yang kamu buat sebelumnya

app = Flask(__name__)
CORS(app)

# Load model
classifier = TeaLeafClassifier()
classifier.load_model("knn_model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image_file = request.files['image']
    filename = secure_filename(image_file.filename)
    image_path = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    image_file.save(image_path)

    # Load & predict
    image = cv2.imread(image_path)
    result = classifier.predict(image)
    if result['class'] == "non_tea":
        return jsonify({"class": "non_tea", "confidence": float(result['confidence']), "message": "Ini bukan daun teh, silakan ganti gambar."})
    else:
        return jsonify({"class": result['class'], "confidence": float(result['confidence'])})

if __name__ == '__main__':
    app.run(debug=True)
