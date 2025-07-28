# app_combined.py
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import joblib
import cv2
import os
import logging
from skimage.feature import graycomatrix, graycoprops
from sklearn.preprocessing import StandardScaler

# Setup
app = Flask(__name__)
cnn_model = load_model("cnn_model.h5")
knn_data = joblib.load("knn_model.pkl")
knn_model = knn_data["model"]
scaler = knn_data["scaler"]
categories = knn_data["categories"]

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Feature extraction
def extract_color_features(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_mean, h_std = np.mean(hsv[:,:,0]), np.std(hsv[:,:,0])
    s_mean, s_std = np.mean(hsv[:,:,1]), np.std(hsv[:,:,1])
    v_mean, v_std = np.mean(hsv[:,:,2]), np.std(hsv[:,:,2])
    return [h_mean, h_std, s_mean, s_std, v_mean, v_std]

def extract_texture_features(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    glcm = graycomatrix(gray, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4], 256, symmetric=True, normed=True)
    contrast = graycoprops(glcm, 'contrast').flatten()
    dissimilarity = graycoprops(glcm, 'dissimilarity').flatten()
    homogeneity = graycoprops(glcm, 'homogeneity').flatten()
    energy = graycoprops(glcm, 'energy').flatten()
    correlation = graycoprops(glcm, 'correlation').flatten()
    return np.concatenate([contrast, dissimilarity, homogeneity, energy, correlation])

def extract_shape_features(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return np.zeros(4)
    largest = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest)
    perimeter = cv2.arcLength(largest, True)
    circularity = 4 * np.pi * area / (perimeter**2) if perimeter > 0 else 0
    x, y, w, h = cv2.boundingRect(largest)
    aspect_ratio = float(w) / h if h > 0 else 0
    return np.array([area, perimeter, circularity, aspect_ratio])

def extract_all_features(img):
    try:
        img = cv2.resize(img, (100, 100))
        color = extract_color_features(img)
        blurred = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (5,5), 0)
        texture = extract_texture_features(img)
        shape = extract_shape_features(blurred)
        return np.concatenate([color, texture, shape])
    except Exception as e:
        logger.error(f"Feature extraction failed: {e}")
        return None

# Flask routes
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        file = request.files["image"]
        if file:
            image = Image.open(file.stream).convert("RGB")
            img_resized = image.resize((64, 64))
            img_array = img_to_array(img_resized) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # CNN prediction: daun teh atau bukan
            is_teh = cnn_model.predict(img_array)[0][0] > 0.5

            if not is_teh:
                result = "🚫 Gambar ini *bukan* daun teh."
            else:
                image_np = np.array(image)
                features = extract_all_features(image_np)
                if features is not None:
                    features_scaled = scaler.transform([features])
                    pred = knn_model.predict(features_scaled)[0]
                    result = f"✅ Daun teh - Tingkat kematangan: **{categories[pred].upper()}**"
                else:
                    result = "⚠️ Gagal ekstraksi fitur dari gambar."

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
