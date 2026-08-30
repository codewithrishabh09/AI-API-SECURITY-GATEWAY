from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import logging

logger = logging.getLogger(__name__)

class Evaluator:
    """Evaluate model performance"""
    
    @staticmethod
    def evaluate(model, X_test, y_test):
        """Evaluate model"""
        predictions = model.predict(X_test)
        
        return {
            'accuracy': accuracy_score(y_test, predictions),
            'precision': precision_score(y_test, predictions, zero_division=0),
            'recall': recall_score(y_test, predictions, zero_division=0),
            'f1': f1_score(y_test, predictions, zero_division=0),
            'confusion_matrix': confusion_matrix(y_test, predictions).tolist()
        }
    
    @staticmethod
    def print_metrics(metrics: dict):
        """Print metrics"""
        logger.info(f"Accuracy: {metrics['accuracy']:.4f}")
        logger.info(f"Precision: {metrics['precision']:.4f}")
        logger.info(f"Recall: {metrics['recall']:.4f}")
        logger.info(f"F1 Score: {metrics['f1']:.4f}")