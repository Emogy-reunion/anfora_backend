from datetime import datetime
import os
from flask import render_template
#import db
#from .models import GeneratedLetter


class LetterService:

  @staticmethod
  def generate_safari_quotation_letter(client_data: dict) -> GeneratedLetter:
    letter_title = (
        f"Official Quotation for {client_data.get('project_name')}"
    )
    recipient = client_data.get("email")

    
    file_dir = "storage/letters"
    os.makedirs(file_dir, exist_ok=True)
    
    file_name = f"quotation_{client_data.get('client_id')}_{int(datetime.utcnow().timestamp())}.pdf"
    file_path = os.path.join(file_dir, file_name)

   
    html_content = render_template('letters/quotation_template.html', data=client_data)
    pdfkit.from_string(html_content, file_path)

    
    db_letter = GeneratedLetter(
        letter_type="quotation_notice",
        recipient_email=recipient,
        subject=letter_title,
        file_path=file_path,
        status="Generated",
    )

    db.session.add(db_letter)
    db.session.commit()
    db.session.refresh(db_letter)

    return db_letter