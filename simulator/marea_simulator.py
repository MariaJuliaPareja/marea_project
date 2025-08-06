#Imports
import json
import time
import random
import requests
import numpy as np
from datetime import datetime

#Class which will work as a simulation of the sensors 
class MAREASimulator:
    #Initiating the class
    def __init__(self):
        #Examples of devices, th
        self.devices = {
            "MAREA_001": {"lat": -12.0464, "lon": -77.0428, "name": "Lima Coast"},
            "MAREA_002": {"lat": -12.0500, "lon": -77.0500, "name": "Callao Bay"},
            "MAREA_003": {"lat": -12.0400, "lon": -77.0350, "name": "Miraflores"}
        }
        #Loading API
        self.api_url = "http://localhost:8000/api/sensor-data"
        #Default levels of contamination
        self.contamination_active = False
        self.contamination_device = None
    #Function to generate normal readings
    def generate_normal_reading(self, device_id):
        device = self.devices[device_id]
        
        return {
            "device_id": device_id,
            "timestamp": time.time(),
            "location": {
                "latitude": device["lat"] + random.uniform(-0.001, 0.001),
                "longitude": device["lon"] + random.uniform(-0.001, 0.001)
            },
            "sensors": { #Information as an example 
                "ph": round(random.uniform(7.8, 8.4), 2),
                "dissolved_oxygen": round(random.uniform(6.0, 8.5), 2),
                "hydrocarbons": round(random.uniform(0.0, 2.0), 1),
                "temperature": round(random.uniform(15.0, 25.0), 1),
                "turbidity": round(random.uniform(1.0, 15.0), 1),
                "conductivity": round(random.uniform(50000, 55000), 0),
                "fluorescence": round(random.uniform(0.0, 0.5), 2)
            },
            "system": { #Clasifications of the alerts as an example
                "battery_level": round(random.uniform(85, 100), 1),
                "threat_level": "NORMAL",
                "confidence": round(random.uniform(0.85, 0.95), 2)
            }
        }
    
   
    if __name__ == "__main__":
        main()