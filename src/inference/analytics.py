from flask import Blueprint, jsonify

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics/summary", methods=["GET"])
def analytics_summary():
    """
    Dummy analytics summary (can be replaced with DB later)
    """
    data = {
        "shipping_comparison": {
            "Local": 78.4,
            "International": 65.2
        },
        "weight_vs_score": [
            {"weight": 1, "score": 82},
            {"weight": 5, "score": 79},
            {"weight": 10, "score": 74},
            {"weight": 20, "score": 68}
        ]
    }

    return jsonify({
        "status": "success",
        "data": data
    })
