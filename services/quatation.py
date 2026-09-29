#uinstall the db pia 
#make sure umeimport the quatationitem na quatation model
#na model ya costing sheet pia


class QuotationService:

  @staticmethod
  def create_quotation(data: dict) -> Quotation:
    subtotal = 0.0
    processed_items = []

    
    for item in data.get("items", []):
      line_total = item["quantity"] * item["unit_price"]
      subtotal += line_total
      processed_items.append(
          QuotationItem(
              description=item["description"],
              quantity=item["quantity"],
              unit_price=item["unit_price"],
              total_price=line_total,
          )
      )

    
    tax_amount = subtotal * 0.16
    total_amount = subtotal + tax_amount

    
    quotation_number = f"QT-{id(data) % 10000:04d}"

    new_quotation = Quotation(
        quotation_number=quotation_number,
        client_id=data["client_id"],
        expiry_date=data.get("expiry_date"),
        notes=data.get("notes"),
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,
        status="Draft",
        items=processed_items,
    )

    db.session.add(new_quotation)
    db.session.commit()
    db.session.refresh(new_quotation)
    return new_quotation

  @staticmethod
  def create_from_cost_sheet(cost_sheet_id: int) -> Quotation:
  

    cost_sheet = db.session.get(CostSheet, cost_sheet_id)
    if not cost_sheet:
      raise ValueError("Cost sheet not found")

    processed_items = []
    subtotal = 0.0

    for cost_item in cost_sheet.items:
      unit_selling_price = cost_item.unit_cost * (
          1 + (cost_sheet.markup_percentage / 100.0)
      )
      line_total = cost_item.quantity * unit_selling_price
      subtotal += line_total

      processed_items.append(
          QuotationItem(
              description=cost_item.description,
              quantity=cost_item.quantity,
              unit_price=unit_selling_price,
              total_price=line_total,
          )
      )

    tax_amount = subtotal * 0.16
    total_amount = subtotal + tax_amount
    quotation_number = f"QT-CS-{cost_sheet.id}-{id(cost_sheet) % 1000:03d}"

    new_quotation = Quotation(
        quotation_number=quotation_number,
        client_id=cost_sheet.client_id,
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,
        status="Draft",
        items=processed_items,
    )

    db.session.add(new_quotation)
    db.session.commit()
    db.session.refresh(new_quotation)
    return new_quotation