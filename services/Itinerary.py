from core.extensions import db
from core.models import Itinerary, ItineraryDay

class ItineraryService:
    @staticmethod
    def create_itinerary(data: dict) -> Itinerary:
        raw_days = data.get("days", [])
        duration_days = len(raw_days) if isinstance(raw_days, list) else int(data.get("duration_days", 1))
        duration_days = duration_days if duration_days > 0 else 1

        processed_days = []
        for index, day_data in enumerate(raw_days, start=1):
            processed_days.append(
                ItineraryDay(
                    day_number=day_data.get("day_number", index),
                    title=day_data.get("title", f"Day {index} Activity"),
                    description=day_data.get("description", ""),
                    accommodation=day_data.get("accommodation"),
                    meals=day_data.get("meals"),
                )
            )

        new_itinerary = Itinerary(
            title=data.get("title", "Safari Expedition Itinerary"),
            client_id=data.get("client_id"),
            cost_sheet_id=data.get("cost_sheet_id"),
            quotation_id=data.get("quotation_id"),
            duration_days=duration_days,
            status=data.get("status", "Draft"),
            notes=data.get("notes"),
            days=processed_days,
        )

        db.session.add(new_itinerary)
        db.session.commit()
        db.session.refresh(new_itinerary)
        return new_itinerary