from sqlalchemy.orm import Session
from app.models.usage import Usage
from app.models.request import Request
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class UsageService:
    
    @staticmethod
    def get_project_usage(db: Session, project_id: int, days: int = 30) -> dict:
        """Get project usage statistics"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        requests = db.query(Request).filter(
            Request.project_id == project_id,
            Request.created_at >= start_date
        ).all()
        
        total_requests = len(requests)
        approved = len([r for r in requests if r.status == "approved"])
        blocked = len([r for r in requests if r.status == "blocked"])
        failed = len([r for r in requests if r.status == "failed"])
        total_tokens = sum([r.tokens_used for r in requests if r.tokens_used])
        total_cost = sum([r.cost for r in requests if r.cost])
        
        return {
            "period_days": days,
            "total_requests": total_requests,
            "approved_requests": approved,
            "blocked_requests": blocked,
            "failed_requests": failed,
            "total_tokens": total_tokens,
            "total_cost": round(total_cost, 2)
        }
    
    @staticmethod
    def get_daily_usage(db: Session, project_id: int, start_date: datetime, end_date: datetime) -> list:
        """Get daily usage breakdown"""
        requests = db.query(Request).filter(
            Request.project_id == project_id,
            Request.created_at >= start_date,
            Request.created_at <= end_date
        ).all()
        
        # Group by date
        daily_stats = {}
        for req in requests:
            date_key = req.created_at.date().isoformat()
            if date_key not in daily_stats:
                daily_stats[date_key] = {
                    "date": date_key,
                    "requests": 0,
                    "tokens": 0,
                    "cost": 0.0
                }
            daily_stats[date_key]["requests"] += 1
            daily_stats[date_key]["tokens"] += req.tokens_used or 0
            daily_stats[date_key]["cost"] += req.cost or 0.0
        
        return sorted(daily_stats.values(), key=lambda x: x["date"])