from datetime import date, timedelta
#make sure to import the invoice na the quotation models and db session
#nimespell quotation wrong kwa kuname files btw

class InvoiceService:

  @staticmethod
  def create_invoice(data: dict) -> Invoice:
    subtotal = 0.0
    processed_items = []

    
    for item in data.get("items", []):
      line_total = item["quantity"] * item["unit_price"]
      subtotal += line_total
      processed_items.append(
          InvoiceItem(
              description=item["description"],
              quantity=item["quantity"],
              unit_price=item["unit_price"],
              total_price=line_total,
          )
      )

    tax_amount = subtotal * 0.16  
    total_amount = subtotal + tax_amount

    due_date_str = data.get("due_date")
    due_date = (
        date.fromisoformat(due_date_str)
        if due_date_str
        else (date.today() + timedelta(days=30))
    )

    invoice_number = f"INV-{id(data) % 10000:04d}"

    new_invoice = Invoice(
        invoice_number=invoice_number,
        quotation_id=data.get("quotation_id"),
        client_id=data["client_id"],
        status="Unpaid",
        issue_date=date.today(),
        due_date=due_date,
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,
        amount_paid=0.0,
        balance_due=total_amount,
        notes=data.get("notes"),
        items=processed_items,
    )

    db.session.add(new_invoice)
    db.session.commit()
    db.session.refresh(new_invoice)
    return new_invoice

  @staticmethod
  def create_from_quotation(quotation_id: int) -> Invoice:
   

    quotation = db.session.get(Quotation, quotation_id)
    if not quotation:
      raise ValueError("Quotation not found")

    processed_items = []
    for q_item in quotation.items:
      processed_items.append(
          InvoiceItem(
              description=q_item.description,
              quantity=q_item.quantity,
              unit_price=q_item.unit_price,
              total_price=q_item.total_price,
          )
      )

    invoice_number = f"INV-QT-{quotation.id}-{id(quotation) % 1000:03d}"
    due_date = date.today() + timedelta(days=30)

    new_invoice = Invoice(
        invoice_number=invoice_number,
        quotation_id=quotation.id,
        client_id=quotation.client_id,
        status="Unpaid",
        issue_date=date.today(),
        due_date=due_date,
        subtotal=quotation.subtotal,
        tax_amount=quotation.tax_amount,
        total_amount=quotation.total_amount,
        amount_paid=0.0,
        balance_due=quotation.total_amount,
        notes=quotation.notes,
        items=processed_items,
    )

    db.session.add(new_invoice)
    db.session.commit()
    db.session.refresh(new_invoice)
    return new_invoice