from flask import Flask, jsonify,request
from datetime import datetime

app.route('/invoice/auto/generate', methods=[POST])
def generate_invoive():
  
  data=request.jsonify
  
  logo_url=data.get('logo_url')
  client_name=data.get('client_name')
  days=data.get('days')
  
  overnight_cost=float(data.get('overnight_cost',0.0))
  src_count=float(data.get('src_count',0))
  psv_km=float(data.get('psv_km',0.0))
  
  vehicle_cost=int(data.get('vehicle_cost'))
  
  total_days=len(days) if len(days) > 0 else 1
  num_people=int(data.get('num_people',1))
  
  
  src_rate=float(data.get(src_rate),0)
  psv_rate=float(data.get(psv_rate))
  
  #Hesabu kidogo tu 
  total_accommodation=num_people * overnight_cost* total_days
  total_srs=src_count*src_rate
  raw_transport= psv_km*psv_km
  pf_markup=raw_transport*1.10
  driver_cost=vehicle_cost*total_days
  
  total_cost=total_srs + pf_markup + driver_cost + total_accommodation
  grand_total=total_cost
  
  return jsonify({
        "status": "success",
        "company_branding": {
            "logo_url": logo_url 
        },
        "invoice_metadata": {
            "client_name": client_name,
            "date_created": datetime.now().strftime("%Y-%m-%d"),
            "duration_days": total_days,
            "itinerary_breakdown": days
        },
        "breakdown": {
            "accommodation": round(total_accommodation, 2),
            "single_supplement_srs": round(total_srs, 2),
            "transport_pf_km_10_percent": round(pf_markup, 2),
            "vehicle_driver": round(driver_cost, 2)
        },
        "totals": {
            "subtotal": round(total_cost, 2),
            "grand_total": round(grand_total, 2)
        }
    }), 200
    
app.route('/invoice/delete/<int:invoice_id', method=[DELETE])
def delete_invoice():
  invoice.query.filter_by(id=invoice_id).delete()
  
  return jsonify({
   'status':'delete',
   'message':'f{invoice_id} has been successfully deleted'
  })
  
app.route('invoice/update/<int:invoice_id>', methods=['PUT','PATCH'])
def update_invoice():
  data=request.json
  
  Malebo=Invoice.query.get_or_404(invoice_id)
  update_fields=list(data.keys())
  return jsonify({
    'status':'updated',
    'message':f'Invoice has been updated'
    
  })
#vibes only