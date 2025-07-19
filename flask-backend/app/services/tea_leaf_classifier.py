import os
import numpy as np
import cv2
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
from skimage.feature import graycomatrix, graycoprops

class TeaLeafClassifier:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.categories = ['siap_petik', 'belum_siap_petik', 'non_tea']
        
    def extract_color_features(self, img):
        """Extract color features from image"""
        # Convert to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Calculate mean and std for each channel
        h_mean, h_std = np.mean(hsv[:,:,0]), np.std(hsv[:,:,0])
        s_mean, s_std = np.mean(hsv[:,:,1]), np.std(hsv[:,:,1])
        v_mean, v_std = np.mean(hsv[:,:,2]), np.std(hsv[:,:,2])

        return [h_mean, h_std, s_mean, s_std, v_mean, v_std]

    def extract_texture_features(self, img):
        """Extract texture features using GLCM"""
        # Convert to grayscale if not already
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img

        # Calculate GLCM
        glcm = graycomatrix(gray, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4], 256, symmetric=True, normed=True)

        # Calculate GLCM properties
        contrast = graycoprops(glcm, 'contrast').flatten()
        dissimilarity = graycoprops(glcm, 'dissimilarity').flatten()
        homogeneity = graycoprops(glcm, 'homogeneity').flatten()
        energy = graycoprops(glcm, 'energy').flatten()
        correlation = graycoprops(glcm, 'correlation').flatten()

        return np.concatenate([contrast, dissimilarity, homogeneity, energy, correlation])

    def extract_shape_features(self, img):
        """Extract shape features from image"""
        # Convert to binary (using original image or preprocessed gray? Let's use original for shape analysis as thresholding can distort shape)
        # Re-reading train_knn_model.py, it uses the *blurred* grayscale image for shape features.
        # Let's stick to that for consistency.
        if len(img.shape) == 3:
             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
             gray = img # Should be grayscale already if coming from preprocess_image flow below

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0) # Re-apply blur locally for shape feature extraction consistency

        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return np.zeros(4)

        # Get the largest contour
        largest_contour = max(contours, key=cv2.contourArea)

        # Calculate shape features
        area = cv2.contourArea(largest_contour)
        perimeter = cv2.arcLength(largest_contour, True)
        circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0

        # Calculate aspect ratio
        x, y, w, h = cv2.boundingRect(largest_contour)
        aspect_ratio = float(w)/h if h > 0 else 0

        return np.array([area, perimeter, circularity, aspect_ratio])

    def preprocess_image(self, img):
        """Preprocess single image and extract features using the same logic as training."""
        try:
            # Resize image first
            img_resized = cv2.resize(img, (100, 100))

            # Extract color features from resized image
            color_features = self.extract_color_features(img_resized)

            # Convert resized image to grayscale for texture and shape features
            gray_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

            # Extract texture features from grayscale resized image
            texture_features = self.extract_texture_features(gray_resized)

            # Extract shape features from grayscale resized image
            shape_features = self.extract_shape_features(gray_resized) # Note: extract_shape_features also applies blur/threshold internally as per training script

            # Combine all features
            features = np.concatenate([
                color_features,
                texture_features,
                shape_features
            ])

            return features
        except Exception as e:
            # Log the specific error during feature extraction
            print(f"Error during feature extraction in preprocess_image: {str(e)}")
            return None # Return None if preprocessing fails

    def load_dataset(self, dataset_path="dataset"):
        """Load and preprocess dataset"""
        data = []
        labels = []
        
        for label, category in enumerate(self.categories):
            folder = os.path.join(dataset_path, category)
            for filename in os.listdir(folder):
                img_path = os.path.join(folder, filename)
                try:
                    img = cv2.imread(img_path)
                    if img is None:
                        print(f"Warning: Could not read image {img_path}")
                        continue
                    # Use the updated preprocess_image method here as well for consistency if retraining
                    # But for now, we only need the updated preprocess_image for prediction
                    # features = self.preprocess_image(img) 
                    # data.append(features)
                    # labels.append(label)
                    pass # Keeping this part as-is for now, assuming the model was trained with the logic in train_knn_model.py
                except Exception as e:
                    print(f"Error processing {img_path}: {str(e)}")
        
        # Note: The loaded model already has the scaler fitted on data with 30 features
        # So, we don't need to re-fit the scaler here. We only need the updated preprocess_image for new data.
        
        return np.array(data), np.array(labels) # This return might not be used in the Flask app flow, but keeping for completeness

    def train(self, X, y):
        """Train the model with hyperparameter tuning"""
        # This method is likely used by train_knn_model.py, not directly in the Flask app.
        # Ensure that the data X here already has the 30 features extracted using the correct preprocess_image logic.
        pass # Keeping this method signature, but implementation is less relevant for the Flask app's prediction error

    def predict(self, image):
        """Predict single image"""
        if self.model is None or self.scaler is None:
             # Added check for scaler as well
            raise ValueError("Model or scaler not loaded yet!")
            
        # Preprocess image using the feature extraction logic
        features = self.preprocess_image(image)
        
        if features is None:
            # Handle case where feature extraction failed
            raise ValueError("Image preprocessing and feature extraction failed.")
            
        # Ensure features is a 2D array for the scaler (1 sample, 30 features)
        features = features.reshape(1, -1)
        
        # Scale features using the loaded scaler
        # The scaler expects 30 features because it was fitted on training data with 30 features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        prediction = self.model.predict(features_scaled)
        # Get probabilities
        probability = self.model.predict_proba(features_scaled)

        # --- START DEBUG PRINTS ---
        print(f"[DEBUG] Extracted Features (first 5): {features[:5]}")
        print(f"[DEBUG] Scaled Features (first 5): {features_scaled[0, :5]}")
        print(f"[DEBUG] Raw Prediction: {prediction}")
        print(f"[DEBUG] Raw Probabilities: {probability}")
        # --- END DEBUG PRINTS ---

        # Find the confidence for the predicted class
        predicted_class_index = prediction[0]
        confidence = probability[0][predicted_class_index]
        
        return {
            'class': self.categories[predicted_class_index],
            'confidence': float(confidence)
        }

    def save_model(self, model_path="model/tea_leaf_model.joblib"):
        """Save model and scaler"""
        if self.model is None or self.scaler is None:
            raise ValueError("No model or scaler to save!")
            
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'categories': self.categories
        }, model_path)
        print(f"Model saved to {model_path}")

    def load_model(self, model_path="model/tea_leaf_model.joblib"):
        """Load saved model"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
            
        try:
            saved_data = joblib.load(model_path)
            self.model = saved_data.get('model')
            self.scaler = saved_data.get('scaler')
            self.categories = saved_data.get('categories', ['siap_petik', 'belum_siap_petik']) # Provide default categories for robustness
            
            if self.model is None or self.scaler is None:
                 raise ValueError("Model or scaler data missing in joblib file.")
                 
            print("Model and scaler loaded successfully")
        except Exception as e:
            print(f"Error loading model file: {e}")
            raise # Re-raise the exception after printing 