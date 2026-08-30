import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

logger = logging.getLogger(__name__)

class Embedder:
    """Create text embeddings"""
    
    def __init__(self, model_type: str = 'tfidf', max_features: int = 1000):
        self.model_type = model_type
        self.max_features = max_features
        self.vectorizer = None
        
        if model_type == 'tfidf':
            self.vectorizer = TfidfVectorizer(max_features=max_features)
    
    def fit(self, texts: list):
        """Fit embedder"""
        self.vectorizer.fit(texts)
        logger.info(f"Embedder fitted with {len(texts)} texts")
    
    def transform(self, texts: list) -> np.ndarray:
        """Transform texts to embeddings"""
        if isinstance(texts, str):
            texts = [texts]
        
        return self.vectorizer.transform(texts).toarray()
    
    def fit_transform(self, texts: list) -> np.ndarray:
        """Fit and transform"""
        return self.vectorizer.fit_transform(texts).toarray()