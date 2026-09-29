from flask import Blueprint, jsonify, request, send_file
import os
#from app import db
# from app.auth.decorators import require_roles 
#from .models import GeneratedLetter
from services.Letters import LetterService

letters_bp = Blueprint("letters", __name__, url_prefix="/letters")


@letters_bp.route("/generate-quotation", methods=["POST"])
def trigger_quotation_letter():
  try:
    data = request.get_json() or {}
    letter_record = LetterService.generate_safari_quotation_letter(data)

    return (
        jsonify({
            "status": "Success",
            "message": "Automated letter successfully generated",
            "letter_id": letter_record.id,
            "file_path": letter_record.file_path,
        }),
        201,
    )
  except Exception as e:
    return jsonify({"status": "Error", "message": str(e)}), 400


@letters_bp.route("/download/<int:letter_id>", methods=["GET"])
def download_letter(letter_id):
  letter = db.session.get(GeneratedLetter, letter_id)
  
  if not letter or not letter.file_path or not os.path.exists(letter.file_path):
    return jsonify({"status": "Error", "message": "Letter file not found"}), 404

  return send_file(
      letter.file_path,
      as_attachment=True,
      download_name=os.path.basename(letter.file_path),
      mimetype="application/pdf",
  )