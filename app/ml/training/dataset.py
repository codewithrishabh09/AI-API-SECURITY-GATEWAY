import pandas as pd
import logging

logger = logging.getLogger(__name__)

class Dataset:
    """Handle training datasets"""
    
    def __init__(self, csv_path: str = None):
        self.data = None
        self.train_data = None
        self.test_data = None
        
        if csv_path:
            self.load_csv(csv_path)
    
    def load_csv(self, path: str):
        """Load dataset from CSV"""
        self.data = pd.read_csv(path)
        logger.info(f"Loaded dataset: {len(self.data)} rows")
        return self.data
    
    def split(self, test_size: float = 0.2, random_state: int = 42):
        """Split into train/test"""
        from sklearn.model_selection import train_test_split
        
        texts = self.data['text'].values
        labels = self.data['label'].values
        
        self.train_data, self.test_data, train_labels, test_labels = train_test_split(
            texts, labels, test_size=test_size, random_state=random_state
        )
        
        logger.info(f"Train: {len(self.train_data)}, Test: {len(self.test_data)}")
        return self.train_data, self.test_data, train_labels, test_labels
    
    def get_stats(self):
        """Get dataset statistics"""
        return {
            'total_samples': len(self.data),
            'columns': list(self.data.columns),
            'label_distribution': self.data['label'].value_counts().to_dict() if 'label' in self.data else None
        }