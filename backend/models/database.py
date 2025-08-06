#Imports
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3
import json
import time
from datetime import datetime
import os

#Flask application
app = Flask(__name__)
CORS(app)

#Creating the Database (It will be an example, later on I have to create it directly on MySQL)
class MAREADatabase:
    #Init of the database (marea_data.db)
    def __init__(self, db_path="data/marea_data.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    #Connect with the new database
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        #With cursor, we execute the commands for the database where we are going to storage 
        #the sensor readings (sensor_readings)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                timestamp REAL NOT NULL,
                latitude REAL,
                longitude REAL,
                turbidity REAL,
                battery_level REAL,
                threat_level TEXT,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        #Other database for the different alerts that will be shown on the app (alerts)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                threat_level TEXT NOT NULL,
                message TEXT,
                latitude REAL,
                longitude REAL,
                resolved BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        #Menssage of successfull database initialized
        print("Database initialized")

        #Sending the data, function reading
        def insert_sensor_reading(self, data): 
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                # Execute and show the data
                cursor.execute('''
                    INSERT INTO sensor_readings 
                    (device_id, timestamp, latitude, longitude, turbidity,
                    battery_level, threat_level, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['device_id'],
                    data['timestamp'],
                    data['location']['latitude'],
                    data['location']['longitude'],
                    data['sensors']['turbidity'],
                    data['system']['battery_level'],
                    data['system']['threat_level'],
                    data['system']['confidence']
                ))
                
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print(f"Error: {e}") #Error exception
                return False
        
        #Function to recive the recent readings
        def get_recent_readings(self, hours=24, device_id=None):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = '''
                SELECT * FROM sensor_readings 
                WHERE timestamp > ?
            '''
            params = [time.time() - (hours * 3600)]
            
            if device_id:
                query += ' AND device_id = ?'
                params.append(device_id)
                
            query += ' ORDER BY timestamp DESC LIMIT 100'
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Convert to dictionaries
            columns = [desc[0] for desc in cursor.description]
            readings = [dict(zip(columns, row)) for row in results]
            
            conn.close()
        return readings
    
    #Creating an Alert and saving on the database of alerts
    def create_alert(self, device_id, alert_type, threat_level, message, latitude, longitude):
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO alerts 
                (device_id, alert_type, threat_level, message, latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (device_id, alert_type, threat_level, message, latitude, longitude))
            
            alert_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return alert_id
    
    #Reading the most recent alerts with 7 days default
    def get_recent_alerts(self, hours=168):  # 7 days default
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, sr.ph, sr.turbidity
            FROM alerts a
            LEFT JOIN sensor_readings sr ON a.device_id = sr.device_id 
            WHERE a.created_at > datetime('now', '-{} hours')
            ORDER BY a.created_at DESC
        '''.format(hours))
        
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        alerts = [dict(zip(columns, row)) for row in results]
        
        conn.close()
        return alerts
    
    