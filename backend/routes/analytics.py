from flask import Blueprint, jsonify
from backend.db import db
from backend.models.prediction import RecommendationLog
from sqlalchemy import func
import logging

analytics_bp = Blueprint('analytics', __name__)
logger = logging.getLogger(__name__)

@analytics_bp.route('/api/analytics/summary', methods=['GET'])
def get_summary():
    """
    Returns summary statistics of all predictions.
    """
    try:
        total_predictions = db.session.query(func.count(RecommendationLog.rec_id)).scalar() or 0
        avg_cost = db.session.query(func.avg(RecommendationLog.cost_prediction)).scalar() or 0
        avg_co2 = db.session.query(func.avg(RecommendationLog.co2_prediction)).scalar() or 0
        
        return jsonify({
            "total_predictions": int(total_predictions),
            "average_cost": float(avg_cost),
            "average_co2": float(avg_co2)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching summary: {e}")
        return jsonify({"error": "Failed to fetch summary"}), 500

@analytics_bp.route('/api/analytics/history', methods=['GET'])
def get_history():
    """
    Returns the last 10 predictions for charting.
    """
    try:
        predictions = RecommendationLog.query.order_by(
            RecommendationLog.created_at.desc()
        ).limit(10).all()
        
        history = [{
            "id": p.rec_id,
            "cost": float(p.cost_prediction) if p.cost_prediction else 0,
            "co2": float(p.co2_prediction) if p.co2_prediction else 0,
            "material_id": p.recommended_material_id,
            "created_at": p.created_at.isoformat() if p.created_at else None
        } for p in reversed(predictions)]  # Reverse to show oldest first
        
        return jsonify({"history": history}), 200
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        return jsonify({"error": "Failed to fetch history"}), 500
