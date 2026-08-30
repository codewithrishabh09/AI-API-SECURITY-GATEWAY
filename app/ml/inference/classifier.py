import logging
from app.ml.models.prompt_classifier import PromptClassifier
from app.ml.models.jailbreak_classifier import JailbreakClassifier
from app.ml.models.toxicity_classifier import ToxicityClassifier

logger = logging.getLogger(__name__)

class MLClassifier:
    """Unified classifier interface"""
    
    def __init__(self):
        self.prompt_classifier = PromptClassifier()
        self.jailbreak_classifier = JailbreakClassifier()
        self.toxicity_classifier = ToxicityClassifier()
    
    def classify_all(self, text: str) -> dict:
        """Run all classifiers"""
        return {
            'prompt_injection': self.prompt_classifier.predict(text),
            'jailbreak': self.jailbreak_classifier.predict(text),
            'toxicity': self.toxicity_classifier.predict(text)
        }
    
    def is_safe(self, text: str, threshold: float = 0.7) -> bool:
        """Check if text is safe"""
        results = self.classify_all(text)
        
        if results['prompt_injection']['confidence'] > threshold:
            if results['prompt_injection']['is_injection']:
                return False
        
        if results['jailbreak']['confidence'] > threshold:
            if results['jailbreak']['is_jailbreak']:
                return False
        
        if results['toxicity']['is_toxic']:
            return False
        
        return True