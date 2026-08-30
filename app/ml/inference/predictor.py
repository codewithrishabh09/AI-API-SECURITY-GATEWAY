import logging
from app.ml.inference.classifier import MLClassifier

logger = logging.getLogger(__name__)

class Predictor:
    """Make predictions on new data"""
    
    def __init__(self):
        self.classifier = MLClassifier()
    
    def predict(self, text: str) -> dict:
        """Make prediction"""
        try:
            classification = self.classifier.classify_all(text)
            is_safe = self.classifier.is_safe(text)
            
            return {
                'text': text[:100] + '...' if len(text) > 100 else text,
                'is_safe': is_safe,
                'classification': classification,
                'risk_score': self._calculate_risk_score(classification)
            }
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return {
                'text': text[:100] + '...' if len(text) > 100 else text,
                'is_safe': True,
                'error': str(e)
            }
    
    @staticmethod
    def _calculate_risk_score(classification: dict) -> float:
        """Calculate overall risk score"""
        score = 0.0
        
        if classification['prompt_injection']['is_injection']:
            score += classification['prompt_injection']['confidence'] * 0.4
        
        if classification['jailbreak']['is_jailbreak']:
            score += classification['jailbreak']['confidence'] * 0.35
        
        if classification['toxicity']['is_toxic']:
            score += 0.25
        
        return min(score, 1.0)