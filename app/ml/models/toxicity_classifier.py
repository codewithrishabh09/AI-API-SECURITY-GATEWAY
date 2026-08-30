import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
import logging

logger = logging.getLogger(__name__)

class ToxicityClassifier:
    """ML model for toxicity detection"""
    
    def __init__(self, model_path: str = None):
        self.model = None
        if model_path:
            self.load_model(model_path)
        else:
            self.initialize_default_model()
    
    def initialize_default_model(self):
        """Initialize default model"""
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=2000, ngram_range=(1, 2))),
            ('classifier', LinearSVC(random_state=42))
        ])
        logger.info("Default toxicity classifier initialized")
    
    def train(self, texts: list, labels: list):
        """Train the model"""
        self.model.fit(texts, labels)
        logger.info(f"Toxicity classifier trained with {len(texts)} samples")
    
    def predict(self, text: str) -> dict:
        """Predict toxicity level"""
        try:
            prediction = self.model.predict([text])[0]
            
            return {
                'is_toxic': bool(prediction),
                'toxicity_level': 'high' if prediction else 'low'
            }
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return {
                'is_toxic': False,
                'toxicity_level': 'low'
            }
    
    def save_model(self, path: str):
        """Save trained model"""
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
        logger.info(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """Load trained model"""
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
        logger.info(f"Model loaded from {path}")