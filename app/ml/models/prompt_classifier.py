import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import logging

logger = logging.getLogger(__name__)

class PromptClassifier:
    """ML model for prompt injection detection"""
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.vectorizer = None
        if model_path:
            self.load_model(model_path)
        else:
            self.initialize_default_model()
    
    def initialize_default_model(self):
        """Initialize default model if no trained model exists"""
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
            ('classifier', MultinomialNB())
        ])
        logger.info("Default prompt classifier initialized")
    
    def train(self, texts: list, labels: list):
        """Train the model"""
        self.model.fit(texts, labels)
        logger.info(f"Prompt classifier trained with {len(texts)} samples")
    
    def predict(self, text: str) -> dict:
        """Predict if text contains prompt injection"""
        try:
            prediction = self.model.predict([text])[0]
            probability = self.model.predict_proba([text])[0]
            
            return {
                'is_injection': bool(prediction),
                'confidence': float(max(probability)),
                'probabilities': {
                    'safe': float(probability[0]),
                    'injection': float(probability[1]) if len(probability) > 1 else 0
                }
            }
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return {
                'is_injection': False,
                'confidence': 0.0,
                'probabilities': {'safe': 1.0, 'injection': 0.0}
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