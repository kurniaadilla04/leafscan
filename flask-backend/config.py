import os

class Config:
    # Flask configuration
    SECRET_KEY = 'dev'
    DEBUG = True
    
    # Model configuration
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'knn_model.pkl')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app', 'static', 'uploads')
    
    # Image processing configuration
    IMAGE_SIZE = (100, 100)  # Size for model input
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# (Removed os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True) from here)
