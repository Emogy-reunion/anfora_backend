#import the db and the models



class CostingSheet:

  @staticmethod
  def calculate_costing_sheet(data: dict) -> CostSheet:
    days = data.get("days", 1)
    total_days = len(days) if isinstance(days, list) else int(days)
    total_days = total_days if total_days > 0 else 1

    accommodation_pp = float(data.get("accommodation", 0.0))
    park_fees = float(data.get("park_fees", 0.0))
    others = float(data.get("others", 0.0))
    num_people = int(data.get("total_people", 1))
    vehicle_cost = float(data.get("vehicle_driver", 0.0))

    
    total_accommodation = total_days * num_people * accommodation_pp
    extra_costs = others * num_people
    total_vehicle_cost = total_days * vehicle_cost
    safe_num_people = num_people if num_people > 0 else 1

    
    price_per_person = (
        total_accommodation
        + park_fees
        + extra_costs
        + (total_vehicle_cost / safe_num_people)
    )

    profit_markup = float(data.get("profit_markup", 1.2))
    final_total_per_person = price_per_person * profit_markup
    
    
    total_cost_price = price_per_person * safe_num_people
    suggested_selling_price = final_total_per_person * safe_num_people
    target_profit = suggested_selling_price - total_cost_price

    
    processed_items = [
        CostItem(
            category="Accommodation",
            description=f"Lodging for {total_days} days @ {accommodation_pp} pp/night",
            unit_cost=accommodation_pp,
            quantity=float(total_days * safe_num_people),
            total_cost=total_accommodation,
        ),
        CostItem(
            category="Park Fees",
            description="Conservation & Entry Fees",
            unit_cost=park_fees,
            quantity=float(safe_num_people),
            total_cost=park_fees,
        ),
        CostItem(
            category="Transport",
            description=f"Vehicle & Driver Hire for {total_days} days",
            unit_cost=vehicle_cost,
            quantity=float(total_days),
            total_cost=total_vehicle_cost,
        ),
        CostItem(
            category="Others",
            description="Incidental / Extra Expenses",
            unit_cost=others,
            quantity=float(safe_num_people),
            total_cost=extra_costs,
        ),
    ]

    
    new_cost_sheet = CostSheet(
        project_name=data.get("project_name", "Safari Expedition Package"),
        client_id=data.get("client_id"),
        total_cost_price=total_cost_price,
        markup_percentage=((profit_markup - 1) * 100),  # e.g., 1.2 -> 20.0%
        target_profit=target_profit,
        suggested_selling_price=suggested_selling_price,
        status="Draft",
        items=processed_items,
    )

    db.session.add(new_cost_sheet)
    db.session.commit()
    db.session.refresh(new_cost_sheet)
    return new_cost_sheet