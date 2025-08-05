#Imports
from flask import Blueprint, request, jsonify, current_app
import time

#Create blueprint for API routes
api_bp = Blueprint('api', __name__)

@api_bp.route('/sensor-data', methods=['POST'])

#Function as an endpoint to recive the sensor data
def receive_sensor_data():
    try:
        data = request.get_json() #JSON request to recive the data
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        #Validate required fields
        required_fields = ['device_id', 'timestamp', 'location', 'sensors', 'system']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        #Use the database instance from the app
        success = current_app.db.insert_sensor_reading(data)
     
        if not success:
            return jsonify({"error": "Database error"}), 500
        
        #Check if alert is needed
        alert_generated = False
        if data['system']['threat_level'] in ['HIGH', 'CRITICAL']: #Two levels of threat
            alert_generated = True
            #Create alert in database, where we know the threat level, the latitude and longitude
            current_app.db.create_alert(
                data['device_id'],
                'CONTAMINATION_DETECTED',
                data['system']['threat_level'],
                f"Contamination detected: HC={data['sensors']['hydrocarbons']} ppm",
                data['location']['latitude'],
                data['location']['longitude']
            )
            #The use of showing device id would be necesary for a scalable solution
            print(f"ALERT GENERATED: {data['device_id']} - {data['system']['threat_level']}")

        
        