import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import logging

logger = logging.getLogger(__name__)

class JailbreakClassifier:
    """ML model for jailbreak attempt detection"""
    
    def __init__(self, model_path: str = None):
        self.model = None
        if model_path:
            self.load_model(model_path)
        else:
            self.initialize_default_model()
    
    def initialize_default_model(self):
        """Initialize default model"""
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1500, ngram_range=(1, 3))),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        logger.info("Default jailbreak classifier initialized")
    
    def train(self, texts: list, labels: list):
        """Train the model"""
        self.model.fit(texts, labels)
        logger.info(f"Jailbreak classifier trained with {len(texts)} samples")
    
    def predict(self, text: str) -> dict:
        """Predict if text contains jailbreak attempt"""
        try:
            prediction = self.model.predict([text])[0]
            probability = self.model.predict_proba([text])[0]
            
            return {
                'is_jailbreak': bool(prediction),
                'confidence': float(max(probability)),
                'probabilities': {
                    'safe': float(probability[0]),
                    'jailbreak': float(probability[1]) if len(probability) > 1 else 0
                }
            }
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return {
                'is_jailbreak': False,
                'confidence': 0.0,
                'probabilities': {'safe': 1.0, 'jailbreak': 0.0}
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