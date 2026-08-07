from flask import Blueprint, jsonify, request
from ..services import QuotationService

quotations_bp = Blueprint("quotations", __name__, url_prefix="/quotations")


@quotations_bp.route("/quotation/create", methods=["POST"])
def create_quotation():
  try:
    data = request.get_json()
    quotation = QuotationService.create_quotation(data)
    return jsonify({
        "message": "Quotation created successfully",
        "quotation_number": quotation.quotation_number,
        "total_amount": quotation.total_amount,
    }), 201
  except Exception as e:
    return jsonify({"error": str(e)}), 400


@quotations_bp.route("/from-cost-sheet/<int:cost_sheet_id>", methods=["POST"])
def convert_cost_sheet(cost_sheet_id):
  try:
    quotation = QuotationService.create_from_cost_sheet(cost_sheet_id)
    return jsonify({
        "message": "Cost sheet successfully converted to quotation",
        "quotation_number": quotation.quotation_number,
    }), 201
  except ValueError as e:
    return jsonify({"error": str(e)}), 404
  except Exception as e:
    return jsonify({"error": str(e)}), 400