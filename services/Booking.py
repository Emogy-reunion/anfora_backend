from datetime import date
from core.extensions import db
from core.models import Booking

class BookingService:
    @staticmethod
    def create_booking(data: dict) -> Booking:
        booking_reference = f"BK-{id(data) % 10000:04d}"
        
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")
        
        start_date = date.fromisoformat(start_date_str) if start_date_str else date.today()
        end_date = date.fromisoformat(end_date_str) if end_date_str else start_date

        new_booking = Booking(
            booking_reference=booking_reference,
            client_id=data["client_id"],
            itinerary_id=data.get("itinerary_id"),
            quotation_id=data.get("quotation_id"),
            invoice_id=data.get("invoice_id"),
            start_date=start_date,
            end_date=end_date,
            num_adults=data.get("num_adults", 1),
            num_children=data.get("num_children", 0),
            total_amount=data.get("total_amount", 0.0),
            status=data.get("status", "Pending"),
            notes=data.get("notes"),
        )

        db.session.add(new_booking)
        db.session.commit()
        db.session.refresh(new_booking)
        return new_booking