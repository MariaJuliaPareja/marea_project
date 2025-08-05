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
                ph REAL,
                dissolved_oxygen REAL,
                hydrocarbons REAL,
                temperature REAL,
                turbidity REAL,
                conductivity REAL,
                fluorescence REAL,
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
        print("Database initialized")
        
    