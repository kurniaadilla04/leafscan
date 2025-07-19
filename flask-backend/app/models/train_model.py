import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.tea_leaf_classifier import TeaLeafClassifier

def train_model():
    # Initialize classifier
    classifier = TeaLeafClassifier()
    
    # Load and preprocess dataset
    X, y = classifier.load_dataset()
    
    # Train model
    accuracy, report = classifier.train(X, y)
    
    # Save model
    classifier.save_model()
    
    return accuracy, report

if __name__ == "__main__":
    train_model() 