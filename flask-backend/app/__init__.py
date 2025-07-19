from flask import Flask
from flask_cors import CORS
from config import Config
import os
from app.services.tea_leaf_classifier import TeaLeafClassifier

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Initialize and load classifier
    classifier = TeaLeafClassifier()
    # Load model using the path from config
    model_path = app.config['MODEL_PATH']
    
    try:
        classifier.load_model(model_path)
        # Attach the loaded classifier to the app object
        app.classifier = classifier
        print("Classifier model loaded successfully and attached to app.")
    except FileNotFoundError as e:
        print(f"Error loading model: {e}. Model will not be available.")
        app.classifier = None # Attach None if loading fails
    except Exception as e:
        print(f"An unexpected error occurred while loading the model: {e}")
        app.classifier = None
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    return app