from app.ml.training.dataset import Dataset
from app.ml.models.prompt_classifier import PromptClassifier
from app.ml.models.jailbreak_classifier import JailbreakClassifier
from app.ml.models.toxicity_classifier import ToxicityClassifier
import logging

logger = logging.getLogger(__name__)

class Trainer:
    """Train ML models"""
    
    @staticmethod
    def train_prompt_injection_detector(dataset_path: str, model_save_path: str):
        """Train prompt injection detector"""
        logger.info("Training prompt injection detector...")
        
        dataset = Dataset(dataset_path)
        texts = dataset.data['text'].values
        labels = dataset.data['label'].values
        
        classifier = PromptClassifier()
        classifier.train(texts, labels)
        classifier.save_model(model_save_path)
        
        logger.info("Prompt injection detector training completed")
        return classifier
    
    @staticmethod
    def train_jailbreak_detector(dataset_path: str, model_save_path: str):
        """Train jailbreak detector"""
        logger.info("Training jailbreak detector...")
        
        dataset = Dataset(dataset_path)
        texts = dataset.data['text'].values
        labels = dataset.data['label'].values
        
        classifier = JailbreakClassifier()
        classifier.train(texts, labels)
        classifier.save_model(model_save_path)
        
        logger.info("Jailbreak detector training completed")
        return classifier
    
    @staticmethod
    def train_toxicity_detector(dataset_path: str, model_save_path: str):
        """Train toxicity detector"""
        logger.info("Training toxicity detector...")
        
        dataset = Dataset(dataset_path)
        texts = dataset.data['text'].values
        labels = dataset.data['label'].values
        
        classifier = ToxicityClassifier()
        classifier.train(texts, labels)
        classifier.save_model(model_save_path)
        
        logger.info("Toxicity detector training completed")
        return classifier