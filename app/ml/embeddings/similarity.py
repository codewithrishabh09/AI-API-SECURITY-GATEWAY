from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging

logger = logging.getLogger(__name__)

class SimilarityCalculator:
    """Calculate text similarity"""
    
    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity"""
        similarity = cosine_similarity([vec1], [vec2])[0][0]
        return float(similarity)
    
    @staticmethod
    def find_similar(query: np.ndarray, corpus: list, threshold: float = 0.7) -> list:
        """Find similar texts in corpus"""
        similarities = []
        
        for i, text_vec in enumerate(corpus):
            sim = SimilarityCalculator.cosine_similarity(query, text_vec)
            if sim > threshold:
                similarities.append({
                    'index': i,
                    'similarity': sim
                })
        
        return sorted(similarities, key=lambda x: x['similarity'], reverse=True)