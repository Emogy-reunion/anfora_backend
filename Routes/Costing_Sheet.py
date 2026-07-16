from flask import Flask,request,jsonify
from datetime import datetime

app.route('/costing/mahesabu' method=[POST])
def costing_unit():
  data=request.jsonify
  
  days=int(data.get('days'),1)
  accomodation_pp=float(data.get('accomodation'),0.0)
  park_fees=float(data.get('park_fees'),0.0)
  others=float(data.get('others' 0))
  num_people=int(data.get('total_people'),1) 
  vehicle_cost=float(data.get('vehicle_driver'))
  
  total_days=len(days) if len(days) > 0 else 1
  
  #Kwa mahesabu one two
  total_accomodation=total_days*num_people*accomodation_pp
  extra_costs=others*num_people
  
  total_vehicle_cost=total_days*vehicle_cost
  
  price_per_person=(total_accomodation + park_fees+ others ) + (total_vehicle_cost/1)
  
  price_per_10=total_accomodation + park_fees+ others ) + (total_vehicle_cost/10)
  
  price=total_accomodation + park_fees+ extra_costs ) + (total_vehicle_cost/num_people)
  profit_markup=int(data.get('profit_markup'))
  
  Final_total=price * profit_markup
  
  return jsonify({
    'status':'Cost Calculation complete',
    'message':'Succes'
    
  }),200
  
  
 
 
  
  
  