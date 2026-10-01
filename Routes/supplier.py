from flask import Blueprint, jsonify, request
from services.supplier import SupplierServiceManager
from core.models import Supplier

suppliers_bp = Blueprint("suppliers", __name__)

@suppliers_bp.route("/supplier/create", methods=["POST","GET"])
def create_supplier():
    try:
        data = request.get_json()
        supplier = SupplierServiceManager.create_supplier(data)
        
        return jsonify({
            "message": "Supplier created successfully",
            "supplier_id": supplier.id,
            "name": supplier.name,
            "category": supplier.category,
            "services_count": len(supplier.services)
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@suppliers_bp.route("/suppliers", methods=["GET"])
def get_suppliers():
    try:
        suppliers = Supplier.query.all()
        result = [{
            "id": s.id,
            "name": s.name,
            "category": s.category,
            "email": s.email,
            "phone": s.phone,
            "location": s.location
        } for s in suppliers]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400