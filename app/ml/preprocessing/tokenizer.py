from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import logging

logger = logging.getLogger(__name__)

class Tokenizer:
    """Text tokenization and vectorization"""
    
    def __init__(self, max_features: int = 1000):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=max_features)
        self.count_vectorizer = CountVectorizer(max_features=max_features)
    
    def fit_tfidf(self, texts: list):
        """Fit TF-IDF vectorizer"""
        self.tfidf_vectorizer.fit(texts)
        logger.info(f"TF-IDF vectorizer fitted with {len(texts)} texts")
    
    def transform_tfidf(self, texts: list):
        """Transform texts using TF-IDF"""
        return self.tfidf_vectorizer.transform(texts)
    
    def fit_count(self, texts: list):
        """Fit Count vectorizer"""
        self.count_vectorizer.fit(texts)
        logger.info(f"Count vectorizer fitted with {len(texts)} texts")
    
    def transform_count(self, texts: list):
        """Transform texts using Count vectorizer"""
        return self.count_vectorizer.transform(texts)
    
    def get_vocabulary(self):
        """Get feature names"""
        return self.tfidf_vectorizer.get_feature_names_out()