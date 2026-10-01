from flask import Blueprint, jsonify, request
from services.Booking import BookingService

bookings_bp = Blueprint("bookings", __name__)

@bookings_bp.route("/booking/create", methods=["POST"])
def create_booking():
    try:
        data = request.get_json()
        booking = BookingService.create_booking(data)
        
        return jsonify({
            "message": "Booking created successfully",
            "booking_id": booking.id,
            "booking_reference": booking.booking_reference,
            "status": booking.status,
            "total_amount": booking.total_amount,
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400