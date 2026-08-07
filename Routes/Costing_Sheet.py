from flask import Blueprint, jsonify, request
from ..services import Costing

costings_bp = Blueprint()


@costings_bp.route("/costing-sheet/create", methods=["POST"])
def create_cost_sheet():
  try:
    data = request.get_json()
    cost_sheet = Costing.create_cost_sheet(data)
    return jsonify({
        "message": "Cost sheet created successfully",
        "cost_sheet_id": cost_sheet.id,
        "total_cost_price": cost_sheet.total_cost_price,
        "suggested_selling_price": cost_sheet.suggested_selling_price,
    }), 201
  except Exception as e:
    return jsonify({"error": str(e)}), 400