import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
from sklearn.preprocessing import StandardScaler
import logging
from skimage.feature import graycomatrix, graycoprops
from tqdm import tqdm

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def augment_image(img):
    """Apply data augmentation to image"""
    augmented_images = []
    
    # Original image
    augmented_images.append(img)
    
    # Horizontal flip
    augmented_images.append(cv2.flip(img, 1))
    
    # Vertical flip
    augmented_images.append(cv2.flip(img, 0))
    
    # Rotate 90 degrees
    augmented_images.append(cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE))
    
    # Rotate -90 degrees
    augmented_images.append(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
    
    # Adjust brightness
    bright = cv2.convertScaleAbs(img, alpha=1.2, beta=10)
    augmented_images.append(bright)
    
    # Adjust contrast
    contrast = cv2.convertScaleAbs(img, alpha=1.2, beta=0)
    augmented_images.append(contrast)
    
    # Add slight noise
    noise = np.zeros(img.shape, np.uint8)
    cv2.randn(noise, 0, 10)
    noisy = cv2.add(img, noise)
    augmented_images.append(noisy)
    
    return augmented_images

def extract_color_features(img):
    """Extract color features from image"""
    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Calculate mean and std for each channel
    h_mean, h_std = np.mean(hsv[:,:,0]), np.std(hsv[:,:,0])
    s_mean, s_std = np.mean(hsv[:,:,1]), np.std(hsv[:,:,1])
    v_mean, v_std = np.mean(hsv[:,:,2]), np.std(hsv[:,:,2])
    
    return [h_mean, h_std, s_mean, s_std, v_mean, v_std]

def extract_texture_features(img):
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

def extract_shape_features(img):
    """Extract shape features from image"""
    # Convert to binary
    _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
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

def preprocess_image(img):
    """Preprocess single image and extract features"""
    try:
        # Resize image
        img = cv2.resize(img, (100, 100))
        
        # Extract color features
        color_features = extract_color_features(img)
        
        # Convert to grayscale for texture and shape features
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Extract texture features
        texture_features = extract_texture_features(blurred)
        
        # Extract shape features
        shape_features = extract_shape_features(blurred)
        
        # Combine all features
        features = np.concatenate([
            color_features,
            texture_features,
            shape_features
        ])
        
        return features
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        return None

def load_and_preprocess_data(dataset_path, augment=True):
    """Load and preprocess images from dataset with optional augmentation"""
    data = []
    labels = []
    categories = ['siap_petik', 'belum_siap_petik', 'non_tea']
    
    for label, category in enumerate(categories):
        folder = os.path.join(dataset_path, category)
        logger.info(f"Processing {category} images...")
        
        for filename in tqdm(os.listdir(folder), desc=f"Processing {category}"):
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            img_path = os.path.join(folder, filename)
            try:
                # Read image
                img = cv2.imread(img_path)
                if img is None:
                    logger.warning(f"Could not read image {img_path}")
                    continue
                
                if augment:
                    # Apply augmentation
                    augmented_images = augment_image(img)
                    for aug_img in augmented_images:
                        features = preprocess_image(aug_img)
                        if features is not None:
                            data.append(features)
                            labels.append(label)
                else:
                    # Process original image only
                    features = preprocess_image(img)
                    if features is not None:
                        data.append(features)
                        labels.append(label)
                
            except Exception as e:
                logger.error(f"Error processing {img_path}: {str(e)}")
    
    return np.array(data), np.array(labels)

def extract_hsv_mean(image_path):
    """
    Ekstrak nilai rata-rata H, S, V dari gambar.
    """
    image = cv2.imread(image_path)
    image = cv2.resize(image, (100, 100))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h_mean = np.mean(hsv[:, :, 0])
    s_mean = np.mean(hsv[:, :, 1])
    v_mean = np.mean(hsv[:, :, 2])
    return [h_mean, s_mean, v_mean]

def main():
    # Path to dataset
    dataset_path = "dataset"
    
    logger.info("Loading and preprocessing data...")
    X, y = load_and_preprocess_data(dataset_path, augment=True)
    
    if len(X) == 0:
        logger.error("No valid images found in dataset!")
        return
    
    logger.info(f"Loaded {len(X)} images")
    logger.info(f"Feature vector shape: {X.shape}")
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Create model
    logger.info("Training model...")
    knn = KNeighborsClassifier(
        n_neighbors=5,
        weights='distance',
        metric='euclidean',
        n_jobs=-1
    )
    
    # Perform cross-validation
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(knn, X_train_scaled, y_train, cv=kf, scoring='accuracy')
    
    logger.info("\nCross-validation scores:")
    logger.info(f"Mean CV accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Train final model
    knn.fit(X_train_scaled, y_train)
    
    # Evaluate on test set
    y_pred = knn.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['siap_petik', 'belum_siap_petik', 'non_tea'])
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    logger.info("\nTest Set Evaluation:")
    logger.info(f"Accuracy: {accuracy:.4f}")
    logger.info("\nClassification Report:")
    logger.info(report)
    logger.info("\nConfusion Matrix:")
    logger.info(conf_matrix)
    
    # Save model and scaler
    logger.info("\nSaving model...")
    model_data = {
        'model': knn,
        'scaler': scaler,
        'categories': ['siap_petik', 'belum_siap_petik', 'non_tea']
    }
    joblib.dump(model_data, 'knn_model.pklv2')
    logger.info("Model saved successfully!")

def simple_knn_hsv_example():
    """
    Contoh training KNN sederhana menggunakan fitur HSV dan label.
    """
    import numpy as np
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import train_test_split
    import os

    data = []
    labels = []

    folder_map = {
        "siap_petik": "dataset/siap_petik",
        "belum_siap_petik": "dataset/belum_siap_petik",
        "non_tea": "dataset/non_tea"
    }

    for label, folder in folder_map.items():
        if not os.path.exists(folder):
            continue
        for filename in os.listdir(folder):
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
            path = os.path.join(folder, filename)
            features = extract_hsv_mean(path)
            data.append(features)
            labels.append(label)

    X = np.array(data)
    y = np.array(labels)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_train, y_train)

    # Evaluasi sederhana
    acc = model.score(X_test, y_test)
    print("Akurasi simple KNN HSV:", acc)
    print("Prediksi:", model.predict(X_test))
    print("Label asli:", y_test)

if __name__ == "__main__":
    main()
        # Visualisasi Confusion Matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
                xticklabels=['siap_petik', 'belum_siap_petik', 'non_tea'],
                yticklabels=['siap_petik', 'belum_siap_petik', 'non_tea'])
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    plt.savefig("confusion_matrix.png")  # Simpan sebagai file PNG
    plt.show()
    # Evaluate on test set
    y_pred = knn.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['siap_petik', 'belum_siap_petik', 'non_tea'])
    conf_matrix = confusion_matrix(y_test, y_pred)

    logger.info("\nTest Set Evaluation:")
    logger.info(f"Accuracy: {accuracy:.4f}")
    logger.info("\nClassification Report:")
    logger.info(report)
    logger.info("\nConfusion Matrix:")
    logger.info(conf_matrix)

    # 🔽 Tambahan: Visualisasi confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
                xticklabels=['siap_petik', 'belum_siap_petik', 'non_tea'],
                yticklabels=['siap_petik', 'belum_siap_petik', 'non_tea'])
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    plt.savefig("confusion_matrix.png")     
    plt.show()

    # Save model and scaler
    logger.info("\nSaving model...")
    model_data = {
        'model': knn,
        'scaler': scaler,
        'categories': ['siap_petik', 'belum_siap_petik', 'non_tea']
    }
    joblib.dump(model_data, 'knn_model.pklv2')
    logger.info("Model saved successfully!")


