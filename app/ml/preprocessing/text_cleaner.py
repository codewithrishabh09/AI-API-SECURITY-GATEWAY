import re
import string
import logging

logger = logging.getLogger(__name__)

class TextCleaner:
    """Clean and preprocess text data"""
    
    @staticmethod
    def clean(text: str) -> str:
        """Clean text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters except basic punctuation
        text = re.sub(r'[^\w\s\.\!\?\-]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def normalize(text: str) -> str:
        """Normalize text"""
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove extra spaces
        text = ' '.join(text.split())
        
        return text
    
    @staticmethod
    def tokenize(text: str) -> list:
        """Tokenize text into words"""
        text = TextCleaner.clean(text)
        tokens = text.split()
        return tokens
    
    @staticmethod
    def remove_stopwords(tokens: list, stopwords: list = None) -> list:
        """Remove common stopwords"""
        if stopwords is None:
            stopwords = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
                'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was'
            }
        
        return [token for token in tokens if token not in stopwords]