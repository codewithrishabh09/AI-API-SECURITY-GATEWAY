from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class CostService:
    
    # Pricing models (per 1k tokens)
    PRICING = {
        "gpt-4": 0.03,
        "gpt-3.5-turbo": 0.0015,
        "claude-v1": 0.01,
    }
    
    @staticmethod
    def calculate_cost(model: str, tokens_used: int) -> float:
        """Calculate cost for API call"""
        price_per_1k = CostService.PRICING.get(model, 0.001)
        cost = (tokens_used / 1000) * price_per_1k
        return round(cost, 4)
    
    @staticmethod
    def get_project_costs(db: Session, project_id: int) -> dict:
        """Get cost breakdown for project"""
        # Implementation would aggregate costs from requests
        return {
            "total_cost": 0.0,
            "daily_average": 0.0,
            "by_model": {}
        }