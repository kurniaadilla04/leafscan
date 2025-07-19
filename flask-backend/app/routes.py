from flask import Blueprint, request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
import joblib
import numpy as np
from PIL import Image
import io
import cv2

# Create a blueprint for the routes
main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main.route('/api/predict', methods=['POST'])
def predict():
    try:
        # Access the classifier from the current_app object
        classifier = current_app.classifier
        
        if classifier is None:
            return jsonify({'error': 'Model not loaded.'}), 500

        # Check if file is present in request
        if 'image' not in request.files:
            return jsonify({'error': 'No file part in request'}), 400
        
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Read and process image
        try:
            # Read image file
            file_bytes = file.read()
            nparr = np.frombuffer(file_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return jsonify({'error': 'Could not decode image'}), 400
            
            # Make prediction
            result = classifier.predict(img)
            # Assuming probability was meant to be result['confidence'] from the classifier predict method
            confidence = result.get('confidence', None) # Use .get() for safety
            
            return jsonify({
                'result': result.get('class', 'Unknown'), # Use .get() for safety
                'confidence': float(confidence) if confidence is not None else None
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Error processing image: {str(e)}")
            return jsonify({'error': 'Error processing image'}), 500
            
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    # Save the file to the uploads directory
    file.save(f'app/static/uploads/{file.filename}')
    return jsonify({'message': 'File uploaded successfully'}), 201

@main.route('/files', methods=['GET'])
def list_files():
    import os
    files = os.listdir('app/static/uploads')
    return jsonify(files), 200

@main.route('/health', methods=['GET'])
def health_check():
    # Access the classifier from the current_app object for the health check
    classifier = current_app.classifier
    return jsonify({
        'status': 'healthy',
        'model_loaded': classifier is not None and classifier.model is not None
    }), 200