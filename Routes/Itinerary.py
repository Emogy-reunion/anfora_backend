from flask import Blueprint, jsonify, request
from services.Itinerary import ItineraryService

itineraries_bp = Blueprint("itineraries", __name__)

@itineraries_bp.route("/itinerary/create", methods=["POST"])
def create_itinerary():
    try:
        data = request.get_json()
        itinerary = ItineraryService.create_itinerary(data)
        
        return jsonify({
            "message": "Itinerary created successfully",
            "itinerary_id": itinerary.id,
            "title": itinerary.title,
            "duration_days": itinerary.duration_days,
            "total_days_recorded": len(itinerary.days)
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400