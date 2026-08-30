from abc import ABC, abstractmethod

class SecurityDetector(ABC):
    """Base class for security detectors"""
    
    @abstractmethod
    def detect(self, text: str) -> bool:
        """Detect security threats"""
        pass