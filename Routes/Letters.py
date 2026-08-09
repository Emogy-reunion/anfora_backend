from datetime import datetime
import os
from tempfile import template
from fastapi import HTTPException
from sqlmodel import Session
from jinja2 import Template
from weasyprint import HTML
#from .models import GeneratedLetter


class LetterService:

  @staticmethod
  def generate_safari_quotation_letter(
      db: Session, client_data: dict
  ) -> GeneratedLetter:
    
    
    letter_title = (
        f"Official Quotation for {client_data.get('project_name')}"
    )
    recipient = client_data.get("email")

    
    html_content = template.render(client_data)
    pdf_bytes = HTML(string=html_content).write_pdf()
    
    
    file_dir = "storage/letters"
    os.makedirs(file_dir, exist_ok=True)
    file_name = f"quotation_{client_data.get('client_id')}_{int(datetime.utcnow().timestamp())}.pdf"
    file_path = os.path.join(file_dir, file_name)

    with open(file_path, "wb") as f:
        f.write(pdf_bytes)

    
    db_letter = GeneratedLetter(
        letter_type="quotation_notice",
        recipient_email=recipient,
        subject=letter_title,
        file_path=file_path,
        status="Generated",
    )

    db.add(db_letter)
    db.commit()
    db.refresh(db_letter)

    return db_letter