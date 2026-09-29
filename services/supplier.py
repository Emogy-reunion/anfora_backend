from core.extensions import db
from core.models import Supplier, SupplierServiceItem

class SupplierServiceManager:
    @staticmethod
    def create_supplier(data: dict) -> Supplier:
        raw_services = data.get("services", [])
        
        processed_services = []
        for svc in raw_services:
            processed_services.append(
                SupplierServiceItem(
                    item_name=svc.get("item_name", "General Service"),
                    description=svc.get("description"),
                    unit_cost=float(svc.get("unit_cost", 0.0)),
                    currency=svc.get("currency", "USD")
                )
            )

        new_supplier = Supplier(
            name=data.get("name"),
            category=data.get("category", "Accommodation"),
            contact_person=data.get("contact_person"),
            email=data.get("email"),
            phone=data.get("phone"),
            location=data.get("location"),
            payment_terms=data.get("payment_terms"),
            notes=data.get("notes"),
            services=processed_services
        )

        db.session.add(new_supplier)
        db.session.commit()
        db.session.refresh(new_supplier)
        return new_supplier