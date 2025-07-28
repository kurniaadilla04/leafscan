import cv2
import os
import numpy as np
import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical

class TeaLeafClassifier:
    def __init__(self):
        self.cnn_model = None
        self.knn_model = None
        self.class_names = ['belum_siap_petik', 'siap_petik']

    def build_cnn_model(self):
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
            MaxPooling2D(2, 2),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Flatten(),
            Dense(64, activation='relu'),
            Dense(1, activation='sigmoid')  # 1: daun teh, 0: non-teh
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def extract_color_histogram(self, image_path):
        image = load_img(image_path, target_size=(100, 100))
        image = img_to_array(image)
        hsv = cv2.cvtColor(image.astype('uint8'), cv2.COLOR_RGB2HSV)
        hist = cv2.calcHist([hsv], [0, 1, 2], None, [8,8,8], [0,180,0,256,0,256])
        cv2.normalize(hist, hist)
        return hist.flatten()

    def train(self, dataset_path='dataset'):
        # Train CNN
        train_datagen = ImageDataGenerator(rescale=1./255)
        train_gen = train_datagen.flow_from_directory(
            dataset_path,
            target_size=(64, 64),
            class_mode='binary',
            batch_size=32
        )
        self.cnn_model = self.build_cnn_model()
        self.cnn_model.fit(train_gen, epochs=10)
        self.cnn_model.save('cnn_model.h5')

        # Train KNN
        data = []
        labels = []
        for label in os.listdir(dataset_path):
            folder = os.path.join(dataset_path, label)
            for file in os.listdir(folder):
                path = os.path.join(folder, file)
                features = self.extract_color_histogram(path)
                data.append(features)
                labels.append(label)

        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)
        self.knn_model = KNeighborsClassifier(n_neighbors=3)
        self.knn_model.fit(X_train, y_train)
        joblib.dump(self.knn_model, 'knn_model.pkl')

    def load_model(self, knn_path='knn_model.pkl', cnn_path='cnn_model.h5'):
        self.knn_model = joblib.load(knn_path)
        self.cnn_model = load_model(cnn_path)

    def predict(self, image):
        # Resize and normalize for CNN
        img = cv2.resize(image, (64, 64))
        img_array = img.astype('float32') / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        is_teh = self.cnn_model.predict(img_array)[0][0] > 0.5
        if not is_teh:
            return {"class": "non_tea", "confidence": 1.0}

        # Resize and extract feature for KNN
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        temp_path = 'temp_predict_image.jpg'
        cv2.imwrite(temp_path, image_rgb)
        features = self.extract_color_histogram(temp_path).reshape(1, -1)
        prediction = self.knn_model.predict(features)[0]
        os.remove(temp_path)

        return {"class": prediction, "confidence": 1.0}
