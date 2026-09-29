from flask import Blueprint, jsonify, request
from ..services import Invoices

invoices_bp = Blueprint()


@invoices_bp.route("/invoice/create", methods=["POST"])
def create_invoice():
  try:
    data = request.get_json() or {}
    invoice = Invoices.create_invoice(data)
    return (
        jsonify({
            "status": "Success",
            "message": "Invoice generated successfully",
            "invoice_number": invoice.invoice_number,
            "total_amount": invoice.total_amount,
            "balance_due": invoice.balance_due,
        }),
        201,
    )
  except Exception as e:
    return jsonify({"status": "Error", "message": str(e)}), 400


@invoices_bp.route("/from-quotation/<int:quotation_id>", methods=["POST"])
def convert_quotation_to_invoice(quotation_id):
  try:
    invoice = Invoices.create_from_quotation(quotation_id)
    return (
        jsonify({
            "status": "Success",
            "message": "Quotation successfully converted to invoice",
            "invoice_number": invoice.invoice_number,
            "total_amount": invoice.total_amount,
        }),
        201,
    )
  except ValueError as e:
    return jsonify({"status": "Error", "message": str(e)}), 404
  except Exception as e:
    return jsonify({"status": "Error", "message": str(e)}), 400