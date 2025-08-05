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
        return jsonify({ #The data will be send to verify the reciving data
            "status": "success",
            "message": "Data received successfully",
            "alert_generated": alert_generated,
            "timestamp": time.time()
        }), 200
        
    except Exception as e:
        print(f"Error processing data: {e}")
        return jsonify({"error": "Internal server error"}), 500

#Getting the sensor readings
@api_bp.route('/readings', methods=['GET'])
def get_readings():
    try:
        device_id = request.args.get('device_id')
        hours = int(request.args.get('hours', 24)) #It will be each 24 hours
        
        readings = current_app.db.get_recent_readings(hours=hours, device_id=device_id)
        
        return jsonify({
            "readings": readings,
            "count": len(readings),
            "hours": hours
        })
    except Exception as e: #Exception to show any erros
        print(f"Error getting readings: {e}")
        return jsonify({"error": "Internal server error"}), 500

#Get the active alerts
@api_bp.route('/alerts', methods=['GET'])
def get_alerts():
    try:
        hours = int(request.args.get('hours', 168))  # 7 days default
        alerts = current_app.db.get_recent_alerts(hours=hours)
        
        return jsonify({ #Counting the total of alerts
            "alerts": alerts,
            "count": len(alerts)
        })
    except Exception as e:
        print(f"Error getting alerts: {e}")
        return jsonify({"error": "Internal server error"}), 500

